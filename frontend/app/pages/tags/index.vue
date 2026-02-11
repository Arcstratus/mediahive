<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { Tag } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const tagsApi = useTagsApi()
const toast = useToast()
const { confirm } = useConfirmDialog()

const { data: tags, refresh } = await tagsApi.list('tags')

const columns: TableColumn<Tag>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'resource_count', header: 'Resources' },
  { accessorKey: 'created_at', header: 'Created At' },
  { id: 'actions', header: '' }
]

const modalOpen = ref(false)
const editModalOpen = ref(false)
const editingTag = ref<Tag | null>(null)

function openEditModal(tag: Tag) {
  editingTag.value = tag
  editModalOpen.value = true
}

async function deleteTag(id: number) {
  if (!await confirm({ message: 'Are you sure you want to delete this tag?' })) return
  const { error } = await tagsApi.remove(id)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  await refresh()
}

</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Tags' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Tags</h1>
      <UButton label="Add Tag" icon="i-lucide-plus" @click="modalOpen = true" />
    </div>

    <UTable :data="tags ?? []" :columns="columns">
      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            size="xs"
            @click="openEditModal(row.original)"
          />
          <UButton
            icon="i-lucide-trash-2"
            variant="ghost"
            color="error"
            size="xs"
            @click="deleteTag(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <CreateTagModal v-model:open="modalOpen" @created="refresh" />
    <EditTagModal v-model:open="editModalOpen" :tag="editingTag" @updated="refresh" />
  </div>
</template>
