<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { Bookmark } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const bookmarksApi = useBookmarksApi()
const toast = useToast()
const { confirm } = useConfirmDialog()
const route = useRoute()

const folder = computed(() => {
  const p = route.params.path
  return Array.isArray(p) ? p.join('/') : p
})

const { data: folders } = await bookmarksApi.getFolders('bookmark-detail-folders')
const { treeItems } = useFolderTree(folders)

const page = ref(1)
const perPage = 20
const sorting = ref<{ id: string, desc: boolean }[]>([])

const { data, refresh } = await bookmarksApi.list('folder-bookmarks', () => {
  const query: Record<string, unknown> = {
    page: page.value,
    per_page: perPage,
    folder: folder.value,
  }
  if (sorting.value.length) {
    query.sort_by = sorting.value[0].id
    query.sort_desc = sorting.value[0].desc
  }
  return query
}, { watch: [page, sorting, folder] })

const bookmarks = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

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

const columns: TableColumn<Bookmark>[] = [
  { accessorKey: 'title', header: sortHeader('Title') },
  { accessorKey: 'url', header: sortHeader('URL') },
  { id: 'description', header: 'Description' },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: sortHeader('Created At') },
  { id: 'actions', header: '' }
]

const modalOpen = ref(false)
const editingBookmark = ref<Bookmark | null>(null)

function openEdit(bookmark: Bookmark) {
  editingBookmark.value = bookmark
  modalOpen.value = true
}

async function deleteBookmark(id: number) {
  if (!await confirm({ message: 'Are you sure you want to delete this bookmark?' })) return
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
    <PageBreadcrumb
      :items="[
        { label: 'Bookmarks', to: '/bookmarks' },
        { label: 'Folders', to: '/bookmarks/folders' },
        { label: folder },
      ]"
    />

    <div class="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6">
      <!-- Left panel: folder tree -->
      <div class="hidden lg:block">
        <ClientOnly>
          <UTree
            v-if="treeItems.length"
            :items="treeItems"
            collapsed-icon="i-lucide-folder"
            expanded-icon="i-lucide-folder-open"
          >
            <template #item="{ item }">
              <NuxtLink
                :to="`/bookmarks/folders/${item.value?.path}`"
                class="flex items-center gap-2 w-full truncate"
                :class="item.value?.path === folder ? 'text-primary font-medium' : 'hover:text-primary'"
              >
                <span class="truncate">{{ item.label }}</span>
                <span v-if="item.value?.count" class="text-xs text-muted">({{ item.value.count }})</span>
              </NuxtLink>
            </template>
          </UTree>
        </ClientOnly>
      </div>

      <!-- Right panel: bookmark table -->
      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-bold">{{ folder }}</h2>

        <UTable v-model:sorting="sorting" :data="bookmarks" :columns="columns" :sorting-options="{ manualSorting: true }" :get-row-id="(row: Bookmark) => String(row.id)">
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

        <p v-if="bookmarks.length === 0" class="text-sm text-muted text-center py-8">
          No bookmarks in this folder.
        </p>
      </div>
    </div>

    <BookmarkModal v-model:open="modalOpen" :bookmark="editingBookmark" @saved="refresh" />
  </div>
</template>
