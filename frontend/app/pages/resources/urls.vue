<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

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
  type: string
  url: string | null
  title: string | null
  tags: Tag[]
  created_at: string
}

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

const { public: { apiBase } } = useRuntimeConfig()

const page = ref(1)
const perPage = 20
const filterTag = ref<string>('')

const { data: allTags, refresh: refreshTags } = await useAsyncData<Tag[]>('tags', () =>
  $fetch(`${apiBase}/tags`)
)

const tagFilterOptions = computed(() => [
  { label: 'All', value: '' },
  ...(allTags.value ?? []).map(t => ({ label: t.name, value: t.name }))
])

const { data, refresh } = await useAsyncData<PaginatedResponse>(
  'url-resources',
  () => $fetch(`${apiBase}/resources`, {
    query: {
      type: 'url',
      page: page.value,
      per_page: perPage,
      ...(filterTag.value ? { tag: filterTag.value } : {})
    }
  }),
  { watch: [filterTag, page] }
)

const resources = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

watch(filterTag, () => {
  page.value = 1
})

const columns: TableColumn<Resource>[] = [
  { accessorKey: 'title', header: 'Title' },
  { accessorKey: 'url', header: 'URL' },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: 'Created At' },
  { id: 'actions', header: '' }
]

// Modal state
const modalOpen = ref(false)
const editingResource = ref<Resource | null>(null)
const form = reactive({ title: '', url: '', tags: [] as string[] })

function openCreate() {
  editingResource.value = null
  form.title = ''
  form.url = ''
  form.tags = []
  modalOpen.value = true
}

function openEdit(resource: Resource) {
  editingResource.value = resource
  form.title = resource.title ?? ''
  form.url = resource.url ?? ''
  form.tags = resource.tags.map(t => t.name)
  modalOpen.value = true
}

async function submitForm() {
  if (editingResource.value) {
    await $fetch(`${apiBase}/resources/${editingResource.value.id}`, {
      method: 'PUT',
      body: { title: form.title, url: form.url, tags: form.tags }
    })
  }
  else {
    await $fetch(`${apiBase}/resources`, {
      method: 'POST',
      body: { type: 'url', title: form.title, url: form.url, tags: form.tags }
    })
  }
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
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">URL Resources</h1>
      <UButton label="Add URL" icon="i-lucide-plus" @click="openCreate" />
    </div>

    <div class="flex items-center gap-2">
      <USelectMenu
        v-model="filterTag"
        :items="tagFilterOptions"
        value-key="value"
        placeholder="Filter by tag"
        class="w-48"
      />
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
            @click="deleteResource(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <div v-if="total > perPage" class="flex justify-center">
      <UPagination v-model:page="page" :total="total" :items-per-page="perPage" />
    </div>

    <UModal v-model:open="modalOpen" :title="editingResource ? 'Edit URL' : 'Add URL'">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="Title" name="title">
            <UInput v-model="form.title" placeholder="Resource title" class="w-full" />
          </UFormField>
          <UFormField label="URL" name="url">
            <UInput v-model="form.url" placeholder="https://example.com" class="w-full" />
          </UFormField>
          <UFormField label="Tags" name="tags">
            <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
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
