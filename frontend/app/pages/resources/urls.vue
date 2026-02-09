<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({
  layout: 'dashboard'
})

interface Resource {
  id: number
  type: string
  url: string | null
  title: string | null
  created_at: string
}

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

const { public: { apiBase } } = useRuntimeConfig()

const { data, refresh } = await useAsyncData<PaginatedResponse>('url-resources', () =>
  $fetch(`${apiBase}/resources`, { query: { per_page: 100 } })
)

const resources = computed(() =>
  (data.value?.items ?? []).filter(r => r.type === 'url')
)

const columns: TableColumn<Resource>[] = [
  { accessorKey: 'title', header: 'Title' },
  { accessorKey: 'url', header: 'URL' },
  { accessorKey: 'created_at', header: 'Created At' },
  { id: 'actions', header: '' }
]

// Modal state
const modalOpen = ref(false)
const editingResource = ref<Resource | null>(null)
const form = reactive({ title: '', url: '' })

function openCreate() {
  editingResource.value = null
  form.title = ''
  form.url = ''
  modalOpen.value = true
}

function openEdit(resource: Resource) {
  editingResource.value = resource
  form.title = resource.title ?? ''
  form.url = resource.url ?? ''
  modalOpen.value = true
}

async function submitForm() {
  if (editingResource.value) {
    await $fetch(`${apiBase}/resources/${editingResource.value.id}`, {
      method: 'PUT',
      body: { title: form.title, url: form.url }
    })
  } else {
    await $fetch(`${apiBase}/resources`, {
      method: 'POST',
      body: { type: 'url', title: form.title, url: form.url }
    })
  }
  modalOpen.value = false
  await refresh()
}

async function deleteResource(id: number) {
  if (!confirm('Are you sure you want to delete this resource?')) return
  await $fetch(`${apiBase}/resources/${id}`, { method: 'DELETE' })
  await refresh()
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">URL Resources</h1>
      <UButton label="Add URL" icon="i-lucide-plus" @click="openCreate" />
    </div>

    <UTable :data="resources" :columns="columns">
      <template #url-cell="{ row }">
        <a
          v-if="row.original.url"
          :href="row.original.url"
          target="_blank"
          class="text-primary hover:underline"
        >
          {{ row.original.url }}
        </a>
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
            @click="deleteResource(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <UModal v-model:open="modalOpen" :title="editingResource ? 'Edit URL' : 'Add URL'">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="Title" name="title">
            <UInput v-model="form.title" placeholder="Resource title" class="w-full" />
          </UFormField>
          <UFormField label="URL" name="url">
            <UInput v-model="form.url" placeholder="https://example.com" class="w-full" />
          </UFormField>
        </div>
      </template>

      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton :label="editingResource ? 'Update' : 'Create'" @click="submitForm" />
        </div>
      </template>
    </UModal>
  </div>
</template>
