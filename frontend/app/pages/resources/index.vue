<script setup lang="ts">
import type { TableColumn, TreeItem } from '@nuxt/ui'
import type { Resource, FolderNode } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const ALL_EXTENSIONS = [
  '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg',
  '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts'
]

const { public: { apiBase } } = useRuntimeConfig()
const resourcesApi = useResourcesApi()
const tagsApi = useTagsApi()
const toast = useToast()

const viewMode = ref<'list' | 'tree'>('tree')
const page = ref(1)
const perPage = 20
const filterSearch = ref('')
const filterTags = ref<string[]>([])
const filterExt = ref<string[]>([])
const sorting = ref<{ id: string, desc: boolean }[]>([])

const extOptions = computed(() =>
  ALL_EXTENSIONS.map(e => ({ label: e, value: e }))
)

const { data: allTags, refresh: refreshTags } = await tagsApi.list('resource-tags')

const tagFilterOptions = computed(() =>
  (allTags.value ?? []).map(t => ({ label: t.name, value: t.name }))
)

const { data, refresh } = await resourcesApi.list('all-resources', () => {
  const query: Record<string, unknown> = {
    page: viewMode.value === 'tree' ? 1 : page.value,
    per_page: viewMode.value === 'tree' ? 100 : perPage
  }
  if (filterSearch.value) query.search = filterSearch.value
  if (filterTags.value.length) query.tag = filterTags.value
  if (filterExt.value.length) query.ext = filterExt.value
  if (sorting.value.length) {
    query.sort_by = sorting.value[0].id
    query.sort_desc = sorting.value[0].desc
  }
  return query
}, { watch: [filterSearch, filterTags, filterExt, page, sorting, viewMode] })

const resources = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

watch([filterSearch, filterTags, filterExt], () => {
  page.value = 1
})

function sortHeader(label: string) {
  return ({ column }: { column: { getIsSorted: () => false | 'asc' | 'desc', toggleSorting: (asc: boolean) => void } }) => {
    const isSorted = column.getIsSorted()
    return h(resolveComponent('UButton'), {
      color: 'neutral',
      variant: 'ghost',
      label,
      icon: isSorted
        ? (isSorted === 'asc' ? 'i-lucide-arrow-up-narrow-wide' : 'i-lucide-arrow-down-wide-narrow')
        : 'i-lucide-arrow-up-down',
      class: '-mx-2.5',
      onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
    })
  }
}

const rowSelection = ref<Record<string, boolean>>({})

const selectedCount = computed(() => Object.values(rowSelection.value).filter(Boolean).length)

async function batchDelete() {
  if (!confirm(`Are you sure you want to delete ${selectedCount.value} selected resource(s)?`)) return
  const ids = Object.keys(rowSelection.value).filter(k => rowSelection.value[k]).map(Number)
  const { error } = await resourcesApi.batchDelete(ids)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  rowSelection.value = {}
  await refresh()
}

const UCheckbox = resolveComponent('UCheckbox')

const columns: TableColumn<Resource>[] = [
  {
    id: 'select',
    header: ({ table }) => h(UCheckbox, {
      'modelValue': table.getIsSomePageRowsSelected() ? 'indeterminate' : table.getIsAllPageRowsSelected(),
      'onUpdate:modelValue': (value: boolean) => table.toggleAllPageRowsSelected(!!value),
      'aria-label': 'Select all'
    }),
    cell: ({ row }) => h(UCheckbox, {
      'modelValue': row.getIsSelected(),
      'onUpdate:modelValue': (value: boolean) => row.toggleSelected(!!value),
      'aria-label': 'Select row'
    })
  },
  { id: 'preview', header: 'Preview', size: 80 },
  { accessorKey: 'title', header: sortHeader('Title'), maxSize: 300 },
  { id: 'category', accessorKey: 'category', header: 'Category' },
  { id: 'ext', accessorFn: row => getExtension(row.filename), header: sortHeader('Extension') },
  { id: 'folder', header: 'Folder' },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: sortHeader('Created At') },
  { id: 'actions', header: '' }
]

// Tree view
function buildTree(items: Resource[]): TreeItem[] {
  const root: FolderNode<Resource> = { children: new Map(), items: [] }

  for (const res of items) {
    if (!res.folder) {
      root.items.push(res)
      continue
    }
    const parts = res.folder.split('/').filter(Boolean)
    let node = root
    for (const part of parts) {
      if (!node.children.has(part)) {
        node.children.set(part, { children: new Map(), items: [] })
      }
      node = node.children.get(part)!
    }
    node.items.push(res)
  }

  function toTreeItems(node: FolderNode<Resource>): TreeItem[] {
    const result: TreeItem[] = []
    const sortedFolders = [...node.children.entries()].sort((a, b) => a[0].localeCompare(b[0]))
    for (const [name, child] of sortedFolders) {
      result.push({
        label: name,
        icon: 'i-lucide-folder',
        defaultExpanded: true,
        children: toTreeItems(child),
      })
    }
    for (const res of node.items) {
      result.push({
        label: res.title || res.filename || 'Untitled',
        icon: res.category === 'image' ? 'i-lucide-image' : 'i-lucide-video',
        slot: 'resource-item',
        value: res,
      } as TreeItem)
    }
    return result
  }

  return toTreeItems(root)
}

const treeItems = computed<TreeItem[]>(() => [{
  label: 'Resources',
  icon: 'i-lucide-library',
  defaultExpanded: true,
  children: buildTree(resources.value),
}])

// Edit modal
const modalOpen = ref(false)
const editingResource = ref<Resource | null>(null)

function openEdit(resource: Resource) {
  editingResource.value = resource
  modalOpen.value = true
}

async function deleteResource(id: number) {
  if (!confirm('Are you sure you want to delete this resource?')) return
  const { error } = await resourcesApi.remove(id)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  await refresh()
}

async function removeTag(resource: Resource, tagName: string) {
  const updatedTags = resource.tags.filter(t => t.name !== tagName).map(t => t.name)
  const { error } = await resourcesApi.update(resource.id, { tags: updatedTags })
  if (error) { toast.add({ title: error, color: 'error' }); return }
  await refresh()
}

// Modal states
const uploadOpen = ref(false)
const downloadOpen = ref(false)
const importOpen = ref(false)

async function onRefreshAll() {
  await refresh()
  await refreshTags()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Resources' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Resources</h1>
    </div>

    <div class="flex items-center gap-2">
      <UInput
        v-model="filterSearch"
        placeholder="Search title..."
        icon="i-lucide-search"
        class="w-64"
      />
      <USelectMenu
        v-model="filterExt"
        :items="extOptions"
        value-key="value"
        placeholder="Extension"
        multiple
        class="w-48"
      />
      <USelectMenu
        v-model="filterTags"
        :items="tagFilterOptions"
        value-key="value"
        placeholder="Filter by tags"
        multiple
        class="w-64"
      />
    </div>

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <UButton label="Upload File" icon="i-lucide-upload" @click="uploadOpen = true" />
        <UButton
          label="Import Folder"
          icon="i-lucide-folder-input"
          variant="soft"
          @click="importOpen = true"
        />
        <UButton
          label="Download URL"
          icon="i-lucide-download"
          variant="soft"
          @click="downloadOpen = true"
        />
        <UButton
          :label="selectedCount > 0 ? `Delete Selected (${selectedCount})` : 'Delete Selected'"
          icon="i-lucide-trash-2"
          color="error"
          variant="soft"
          :disabled="selectedCount === 0"
          @click="batchDelete"
        />
      </div>
      <div class="flex items-center gap-2">
        <UButton
          icon="i-lucide-list"
          :variant="viewMode === 'list' ? 'soft' : 'ghost'"
          color="neutral"
          :disabled="viewMode === 'list'"
          @click="viewMode = 'list'"
        />
        <UButton
          icon="i-lucide-folder-tree"
          :variant="viewMode === 'tree' ? 'soft' : 'ghost'"
          color="neutral"
          :disabled="viewMode === 'tree'"
          @click="viewMode = 'tree'"
        />
      </div>
    </div>

    <!-- List View -->
    <template v-if="viewMode === 'list'">
      <UTable v-model:sorting="sorting" v-model:row-selection="rowSelection" :data="resources" :columns="columns" :sorting-options="{ manualSorting: true }" :get-row-id="(row: Resource) => String(row.id)">
        <template #preview-cell="{ row }">
          <img
            v-if="row.original.category === 'image'"
            :src="`${apiBase}/media/${row.original.folder ? row.original.folder + '/' : ''}${row.original.filename}`"
            class="size-10 rounded object-cover"
          >
          <img
            v-else-if="row.original.thumbnail"
            :src="`${apiBase}/thumbnails/${row.original.thumbnail}`"
            class="size-10 rounded object-cover"
          >
          <UIcon v-else name="i-lucide-video" class="size-10 text-muted" />
        </template>

        <template #title-cell="{ row }">
          <span class="block max-w-xs truncate" :title="row.original.title ?? ''">{{ row.original.title }}</span>
        </template>

        <template #category-cell="{ row }">
          <UBadge :label="row.original.category" :color="row.original.category === 'image' ? 'info' : 'warning'" variant="subtle" size="sm" />
        </template>

        <template #ext-cell="{ row }">
          <UBadge :label="getExtension(row.original.filename)" variant="subtle" size="sm" />
        </template>

        <template #folder-cell="{ row }">
          <span v-if="row.original.folder">{{ row.original.folder }}</span>
        </template>

        <template #tags-cell="{ row }">
          <div class="flex gap-1 flex-wrap">
            <UBadge
              v-for="tag in row.original.tags"
              :key="tag.id"
              :label="tag.name"
              variant="subtle"
              size="sm"
              trailing-icon="i-lucide-x"
              class="cursor-pointer"
              @click="removeTag(row.original, tag.name)"
            />
          </div>
        </template>

        <template #created_at-cell="{ row }">
          {{ formatDate(row.original.created_at) }}
        </template>

        <template #actions-cell="{ row }">
          <div class="flex gap-1 justify-end">
            <UButton
              icon="i-lucide-eye"
              variant="ghost"
              color="neutral"
              size="xs"
              :to="`/resources/viewer?id=${row.original.id}`"
            />
            <UButton
              icon="i-lucide-pencil"
              variant="ghost"
              color="neutral"
              size="xs"
              @click="openEdit(row.original)"
            />
            <UButton
              icon="i-lucide-trash-2"
              variant="ghost"
              color="error"
              size="xs"
              @click="deleteResource(row.original.id)"
            />
          </div>
        </template>
      </UTable>

      <div v-if="total > perPage" class="flex justify-center">
        <UPagination v-model:page="page" :total="total" :items-per-page="perPage" />
      </div>
    </template>

    <!-- Tree View -->
    <template v-else>
      <ClientOnly>
        <UTree
          v-if="treeItems.length"
          :items="treeItems"
          size="lg"
          collapsed-icon="i-lucide-folder"
          expanded-icon="i-lucide-folder-open"
        >
          <template #resource-item="{ item }">
            <div class="flex items-center gap-2 group w-full">
              <UIcon
                :name="item.value?.category === 'image' ? 'i-lucide-image' : 'i-lucide-video'"
                class="size-4 text-primary shrink-0"
              />
              <span class="truncate">{{ item.label }}</span>
              <UBadge :label="item.value?.category" :color="item.value?.category === 'image' ? 'info' : 'warning'" variant="subtle" size="xs" class="ml-1" />
              <div v-if="item.value?.tags?.length" class="flex gap-1 ml-2">
                <UBadge
                  v-for="tag in item.value.tags"
                  :key="tag.id"
                  :label="tag.name"
                  variant="subtle"
                  size="xs"
                />
              </div>
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <UButton
                  icon="i-lucide-eye"
                  variant="ghost"
                  color="neutral"
                  size="xs"
                  @click.stop="navigateTo(`/resources/viewer?id=${item.value.id}`)"
                />
                <UButton
                  icon="i-lucide-pencil"
                  variant="ghost"
                  color="neutral"
                  size="xs"
                  @click.stop="openEdit(item.value)"
                />
                <UButton
                  icon="i-lucide-trash-2"
                  variant="ghost"
                  color="error"
                  size="xs"
                  @click.stop="deleteResource(item.value.id)"
                />
              </div>
            </div>
          </template>
        </UTree>
        <p v-else class="text-sm text-muted">No resources yet.</p>
      </ClientOnly>
    </template>

    <EditResourceModal v-model:open="modalOpen" :resource="editingResource" @saved="onRefreshAll" />
    <UploadModal v-model:open="uploadOpen" @uploaded="onRefreshAll" />
    <DownloadUrlModal v-model:open="downloadOpen" @downloaded="onRefreshAll" />
    <ImportFolderModal v-model:open="importOpen" @imported="onRefreshAll" />
  </div>
</template>
