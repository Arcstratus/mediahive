<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { Bookmark } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const bookmarksApi = useBookmarksApi()
const tagsApi = useTagsApi()
const toast = useToast()

const page = ref(1)
const perPage = 20
const filterSearch = ref('')
const filterTags = ref<string[]>([])
const sorting = ref<{ id: string, desc: boolean }[]>([])

const { data: allTags, refresh: refreshTags } = await tagsApi.list('tags')

const tagFilterOptions = computed(() =>
  (allTags.value ?? []).map(t => ({ label: t.name, value: t.name }))
)

const { data, refresh } = await bookmarksApi.list('bookmarks', () => {
  const query: Record<string, unknown> = {
    page: page.value,
    per_page: perPage
  }
  if (filterSearch.value) query.search = filterSearch.value
  if (filterTags.value.length) query.tag = filterTags.value
  if (sorting.value.length) {
    query.sort_by = sorting.value[0].id
    query.sort_desc = sorting.value[0].desc
  }
  return query
}, { watch: [filterSearch, filterTags, page, sorting] })

const bookmarks = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

watch([filterSearch, filterTags], () => {
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
  if (!confirm(`Are you sure you want to delete ${selectedCount.value} selected bookmark(s)?`)) return
  const ids = Object.keys(rowSelection.value).filter(k => rowSelection.value[k]).map(Number)
  const { error } = await bookmarksApi.batchDelete(ids)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  rowSelection.value = {}
  await refresh()
}

const UCheckbox = resolveComponent('UCheckbox')

const columns: TableColumn<Bookmark>[] = [
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
  { accessorKey: 'title', header: sortHeader('Title') },
  { accessorKey: 'url', header: sortHeader('URL') },
  { id: 'description', header: 'Description' },
  { id: 'folder', header: 'Folder' },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: sortHeader('Created At') },
  { id: 'actions', header: '' }
]

// Modal state
const modalOpen = ref(false)
const editingBookmark = ref<Bookmark | null>(null)
const importOpen = ref(false)

function openCreate() {
  editingBookmark.value = null
  modalOpen.value = true
}

function openEdit(bookmark: Bookmark) {
  editingBookmark.value = bookmark
  modalOpen.value = true
}

async function onRefreshAll() {
  await refresh()
  await refreshTags()
}

async function deleteBookmark(id: number) {
  if (!confirm('Are you sure you want to delete this bookmark?')) return
  const { error } = await bookmarksApi.remove(id)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  await refresh()
}

async function removeTag(bookmark: Bookmark, tagName: string) {
  const updatedTags = bookmark.tags.filter(t => t.name !== tagName).map(t => t.name)
  const { error } = await bookmarksApi.update(bookmark.id, { tags: updatedTags })
  if (error) { toast.add({ title: error, color: 'error' }); return }
  await refresh()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Bookmarks' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Bookmarks</h1>
    </div>

    <div class="flex items-center gap-2">
      <UInput
        v-model="filterSearch"
        placeholder="Search title, URL, or description..."
        icon="i-lucide-search"
        class="w-64"
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

    <div class="flex items-center gap-2">
      <UButton label="Add" icon="i-lucide-plus" @click="openCreate" />
      <UButton label="Import" icon="i-lucide-file-down" variant="soft" @click="importOpen = true" />
      <UButton
        :label="selectedCount > 0 ? `Delete (${selectedCount})` : 'Delete'"
        icon="i-lucide-trash-2"
        color="error"
        variant="soft"
        :disabled="selectedCount === 0"
        @click="batchDelete"
      />
    </div>

    <UTable v-model:sorting="sorting" v-model:row-selection="rowSelection" :data="bookmarks" :columns="columns" :sorting-options="{ manualSorting: true }" :get-row-id="(row: Bookmark) => String(row.id)">
      <template #title-cell="{ row }">
        <span class="truncate max-w-48 block" :title="row.original.title">{{ row.original.title }}</span>
      </template>

      <template #url-cell="{ row }">
        <a
          :href="row.original.url"
          target="_blank"
          class="text-primary hover:underline truncate max-w-48 block"
          :title="row.original.url"
        >
          {{ row.original.url }}
        </a>
      </template>

      <template #description-cell="{ row }">
        <span v-if="row.original.description" class="truncate max-w-32 block" :title="row.original.description">{{ row.original.description }}</span>
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
            @click="deleteBookmark(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <div v-if="total > perPage" class="flex justify-center">
      <UPagination v-model:page="page" :total="total" :items-per-page="perPage" />
    </div>

    <BookmarkModal v-model:open="modalOpen" :bookmark="editingBookmark" @saved="onRefreshAll" />
    <ImportBookmarksModal v-model:open="importOpen" @imported="onRefreshAll" />
  </div>
</template>
