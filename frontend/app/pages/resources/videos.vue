<script setup lang="ts">
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

const { data, refresh } = await useAsyncData<PaginatedResponse>(
  'video-resources',
  () => $fetch(`${apiBase}/resources`, {
    query: { type: 'video', page: page.value, per_page: perPage }
  }),
  { watch: [page] }
)

const resources = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

// Edit modal
const modalOpen = ref(false)
const editingResource = ref<Resource | null>(null)
const form = reactive({ title: '', tags: [] as string[] })

function openEdit(resource: Resource) {
  editingResource.value = resource
  form.title = resource.title ?? ''
  form.tags = resource.tags.map(t => t.name)
  modalOpen.value = true
}

async function submitForm() {
  if (!editingResource.value) return
  await $fetch(`${apiBase}/resources/${editingResource.value.id}`, {
    method: 'PUT',
    body: { title: form.title, tags: form.tags }
  })
  modalOpen.value = false
  await refresh()
}

async function deleteResource(id: number) {
  if (!confirm('Are you sure you want to delete this video?')) return
  await $fetch(`${apiBase}/resources/${id}`, { method: 'DELETE' })
  await refresh()
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Video Resources</h1>

    <div v-if="resources.length === 0" class="text-muted">
      No videos yet.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard v-for="r in resources" :key="r.id" class="overflow-hidden">
        <template #header>
          <div class="aspect-video bg-muted overflow-hidden">
            <video
              :src="`${apiBase}/media/${r.url}`"
              class="w-full h-full object-cover"
              preload="metadata"
              muted
            />
          </div>
        </template>
        <div class="flex flex-col gap-1">
          <div class="flex items-center justify-between gap-2">
            <p class="text-sm truncate" :title="r.title ?? r.url ?? ''">{{ r.title ?? r.url }}</p>
            <div class="flex gap-1 shrink-0">
              <UButton
                icon="i-lucide-pencil"
                variant="ghost"
                color="neutral"
                size="xs"
                @click="openEdit(r)"
              />
              <UButton
                icon="i-lucide-trash-2"
                variant="ghost"
                color="error"
                size="xs"
                @click="deleteResource(r.id)"
              />
            </div>
          </div>
          <div v-if="r.tags.length" class="flex gap-1 flex-wrap">
            <UBadge
              v-for="tag in r.tags"
              :key="tag.id"
              :label="tag.name"
              variant="subtle"
              size="sm"
            />
          </div>
        </div>
      </UCard>
    </div>

    <div v-if="total > perPage" class="flex justify-center">
      <UPagination v-model:page="page" :total="total" :items-per-page="perPage" />
    </div>

    <UModal v-model:open="modalOpen" title="Edit Video">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="Title" name="title">
            <UInput v-model="form.title" placeholder="Video title" class="w-full" />
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
  </div>
</template>
