<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { Tag } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const tagsApi = useTagsApi()

const { data: tags, refresh } = await tagsApi.list('tags')

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
  await tagsApi.create(newTagName.value.trim())
  modalOpen.value = false
  await refresh()
}

async function deleteTag(id: number) {
  if (!confirm('Are you sure you want to delete this tag?')) return
  await tagsApi.remove(id)
  await refresh()
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
