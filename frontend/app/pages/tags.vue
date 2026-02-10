<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({
  layout: 'dashboard'
})

interface Tag {
  id: number
  name: string
  created_at: string
  resource_count: number
}

const { public: { apiBase } } = useRuntimeConfig()

const { data: tags, refresh } = await useAsyncData<Tag[]>('tags', () =>
  $fetch(`${apiBase}/tags`)
)

const columns: TableColumn<Tag>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'resource_count', header: 'Resources' },
  { accessorKey: 'created_at', header: 'Created At' },
  { id: 'actions', header: '' }
]

const modalOpen = ref(false)
const newTagName = ref('')

function openCreate() {
  newTagName.value = ''
  modalOpen.value = true
}

async function createTag() {
  if (!newTagName.value.trim()) return
  await $fetch(`${apiBase}/tags`, {
    method: 'POST',
    body: { name: newTagName.value.trim() }
  })
  modalOpen.value = false
  await refresh()
}

async function deleteTag(id: number) {
  if (!confirm('Are you sure you want to delete this tag?')) return
  await $fetch(`${apiBase}/tags/${id}`, { method: 'DELETE' })
  await refresh()
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Tags' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Tags</h1>
      <UButton label="Add Tag" icon="i-lucide-plus" @click="openCreate" />
    </div>

    <UTable :data="tags ?? []" :columns="columns">
      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
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

    <UModal v-model:open="modalOpen" title="Add Tag">
      <template #body>
        <UFormField label="Name" name="name">
          <UInput v-model="newTagName" placeholder="Tag name" class="w-full" @keyup.enter="createTag" />
        </UFormField>
      </template>

      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Create" @click="createTag" />
        </div>
      </template>
    </UModal>
  </div>
</template>
