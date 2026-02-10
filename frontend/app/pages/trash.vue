<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { TrashItem } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const { public: { apiBase } } = useRuntimeConfig()

const { data: items, refresh } = await useAsyncData<TrashItem[]>('trash', () =>
  $fetch(`${apiBase}/trash`)
)

const trashItems = computed(() => items.value ?? [])

async function restoreItem(id: number) {
  await $fetch(`${apiBase}/trash/${id}/restore`, { method: 'POST' })
  await refresh()
}

async function deleteItem(id: number) {
  if (!confirm('Permanently delete this resource? This cannot be undone.')) return
  await $fetch(`${apiBase}/trash/${id}`, { method: 'DELETE' })
  await refresh()
}

async function emptyTrash() {
  if (!confirm('Permanently delete all trashed resources? This cannot be undone.')) return
  await $fetch(`${apiBase}/trash`, { method: 'DELETE' })
  await refresh()
}

const columns: TableColumn<TrashItem>[] = [
  { accessorKey: 'title', header: 'Title' },
  { accessorKey: 'filename', header: 'Filename' },
  { accessorKey: 'category', header: 'Category' },
  { id: 'folder', header: 'Folder' },
  { accessorKey: 'deleted_at', header: 'Deleted At' },
  { id: 'actions', header: '' }
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Trash' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Trash</h1>
      <UButton
        label="Empty Trash"
        icon="i-lucide-trash-2"
        color="error"
        variant="soft"
        :disabled="trashItems.length === 0"
        @click="emptyTrash"
      />
    </div>

    <UTable :data="trashItems" :columns="columns">
      <template #title-cell="{ row }">
        <span class="truncate max-w-48 block" :title="row.original.title ?? ''">
          {{ row.original.title ?? row.original.filename }}
        </span>
      </template>

      <template #filename-cell="{ row }">
        <span class="truncate max-w-48 block text-sm text-muted" :title="row.original.filename ?? ''">
          {{ row.original.filename }}
        </span>
      </template>

      <template #folder-cell="{ row }">
        <span v-if="row.original.folder">{{ row.original.folder }}</span>
      </template>

      <template #deleted_at-cell="{ row }">
        {{ formatDate(row.original.deleted_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-undo-2"
            label="Restore"
            variant="soft"
            color="neutral"
            size="xs"
            @click="restoreItem(row.original.id)"
          />
          <UButton
            icon="i-lucide-trash-2"
            label="Delete"
            variant="soft"
            color="error"
            size="xs"
            @click="deleteItem(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <p v-if="trashItems.length === 0" class="text-sm text-muted text-center py-8">
      Trash is empty.
    </p>
  </div>
</template>
