<script setup lang="ts">
import type { TableColumn, TreeItem } from '@nuxt/ui'

definePageMeta({
  layout: 'dashboard'
})

interface Tag {
  id: number
  name: string
  created_at: string
}

interface Resource {
  id: number
  category: string
  filename: string | null
  title: string | null
  folder: string | null
  tags: Tag[]
  created_at: string
}

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

const ALL_EXTENSIONS = [
  '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg',
  '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts'
]

const { public: { apiBase } } = useRuntimeConfig()

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

const { data: allTags, refresh: refreshTags } = await useAsyncData<Tag[]>('resource-tags', () =>
  $fetch(`${apiBase}/tags`)
)

const tagFilterOptions = computed(() =>
  (allTags.value ?? []).map(t => ({ label: t.name, value: t.name }))
)

const { data, refresh } = await useAsyncData<PaginatedResponse>(
  'all-resources',
  () => {
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
    return $fetch(`${apiBase}/resources`, { query })
  },
  { watch: [filterSearch, filterTags, filterExt, page, sorting, viewMode] }
)

const resources = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

watch([filterSearch, filterTags, filterExt], () => {
  page.value = 1
})

function getExtension(filename: string | null): string {
  if (!filename) return ''
  const dot = filename.lastIndexOf('.')
  return dot >= 0 ? filename.slice(dot) : ''
}

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
  await $fetch(`${apiBase}/resources/batch-delete`, {
    method: 'POST',
    body: { ids }
  })
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
  { accessorKey: 'title', header: sortHeader('Title'), maxSize: 300 },
  { id: 'category', accessorKey: 'category', header: 'Category' },
  { id: 'ext', accessorFn: row => getExtension(row.filename), header: sortHeader('Extension') },
  { id: 'folder', header: 'Folder' },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: sortHeader('Created At') },
  { id: 'actions', header: '' }
]

// Tree view
interface FolderNode {
  children: Map<string, FolderNode>
  resources: Resource[]
}

function buildTree(items: Resource[]): TreeItem[] {
  const root: FolderNode = { children: new Map(), resources: [] }

  for (const res of items) {
    if (!res.folder) {
      root.resources.push(res)
      continue
    }
    const parts = res.folder.split('/').filter(Boolean)
    let node = root
    for (const part of parts) {
      if (!node.children.has(part)) {
        node.children.set(part, { children: new Map(), resources: [] })
      }
      node = node.children.get(part)!
    }
    node.resources.push(res)
  }

  function toTreeItems(node: FolderNode): TreeItem[] {
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
    for (const res of node.resources) {
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
const form = reactive({ title: '', folder: '', tags: [] as string[] })

function openEdit(resource: Resource) {
  editingResource.value = resource
  form.title = resource.title ?? ''
  form.folder = resource.folder ?? ''
  form.tags = resource.tags.map(t => t.name)
  modalOpen.value = true
}

async function submitForm() {
  if (!editingResource.value) return
  await $fetch(`${apiBase}/resources/${editingResource.value.id}`, {
    method: 'PUT',
    body: { title: form.title, folder: form.folder || null, tags: form.tags }
  })
  modalOpen.value = false
  await refresh()
  await refreshTags()
}

async function deleteResource(id: number) {
  if (!confirm('Are you sure you want to delete this resource?')) return
  await $fetch(`${apiBase}/resources/${id}`, { method: 'DELETE' })
  await refresh()
}

async function removeTag(resource: Resource, tagName: string) {
  const updatedTags = resource.tags.filter(t => t.name !== tagName).map(t => t.name)
  await $fetch(`${apiBase}/resources/${resource.id}`, {
    method: 'PUT',
    body: { tags: updatedTags }
  })
  await refresh()
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

// Upload modal
const uploadOpen = ref(false)
const uploadFile = ref<File | null>(null)
const uploadForm = reactive({ title: '', tags: [] as string[] })
const uploading = ref(false)

function openUpload() {
  uploadFile.value = null
  uploadForm.title = ''
  uploadForm.tags = []
  uploading.value = false
  uploadOpen.value = true
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  uploadFile.value = input.files?.[0] ?? null
}

async function submitUpload() {
  if (!uploadFile.value) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    if (uploadForm.title) formData.append('title', uploadForm.title)
    if (uploadForm.tags.length) formData.append('tags', uploadForm.tags.join(','))
    await $fetch(`${apiBase}/resources/upload`, {
      method: 'POST',
      body: formData
    })
    uploadOpen.value = false
    await refresh()
    await refreshTags()
  }
  finally {
    uploading.value = false
  }
}

// Download URL modal
const downloadOpen = ref(false)
const downloadUrl = ref('')
const downloading = ref(false)

function openDownload() {
  downloadUrl.value = ''
  downloading.value = false
  downloadOpen.value = true
}

const toast = useToast()

async function submitDownload() {
  if (!downloadUrl.value) return
  downloading.value = true
  try {
    await $fetch(`${apiBase}/resources/download`, {
      method: 'POST',
      body: { url: downloadUrl.value }
    })
    downloadOpen.value = false
    toast.add({ title: 'Download started', description: 'The file is being downloaded in the background.', color: 'info' })
  }
  finally {
    downloading.value = false
  }
}

// Import folder modal
const importOpen = ref(false)

async function onImported() {
  await refresh()
  await refreshTags()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <UBreadcrumb :items="[{ label: 'Resources' }]" />

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
        <UButton label="Upload File" icon="i-lucide-upload" @click="openUpload" />
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
          @click="openDownload"
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

    <!-- Edit modal -->
    <UModal v-model:open="modalOpen" title="Edit Resource">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="Title" name="title">
            <UInput v-model="form.title" placeholder="Resource title" class="w-full" />
          </UFormField>
          <UFormField label="Folder" name="folder">
            <UInput v-model="form.folder" placeholder="e.g. 2024/vacation" class="w-full" />
          </UFormField>
          <UFormField label="Tags" name="tags">
            <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
          </UFormField>
        </div>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Update" @click="submitForm" />
        </div>
      </template>
    </UModal>

    <!-- Upload modal -->
    <UModal v-model:open="uploadOpen" title="Upload File">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="File" name="file">
            <input type="file" accept="image/*,video/*" @change="onFileChange">
          </UFormField>
          <UFormField label="Title" name="title">
            <UInput v-model="uploadForm.title" placeholder="Title (optional)" class="w-full" />
          </UFormField>
          <UFormField label="Tags" name="tags">
            <UInputTags v-model="uploadForm.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
          </UFormField>
        </div>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Upload" :loading="uploading" :disabled="!uploadFile" @click="submitUpload" />
        </div>
      </template>
    </UModal>

    <!-- Download URL modal -->
    <UModal v-model:open="downloadOpen" title="Download from URL">
      <template #body>
        <UFormField label="URL" name="url">
          <UInput v-model="downloadUrl" placeholder="https://example.com/file.mp4" class="w-full" />
        </UFormField>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Download" :loading="downloading" :disabled="!downloadUrl" @click="submitDownload" />
        </div>
      </template>
    </UModal>

    <!-- Import Folder Modal -->
    <ImportFolderModal v-model:open="importOpen" @imported="onImported" />
  </div>
</template>
