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
  folder: string | null
  tags: Tag[]
  created_at: string
}

const { public: { apiBase } } = useRuntimeConfig()
const route = useRoute()
const router = useRouter()

const ids = ref<number[]>([])
const currentId = ref<number | null>(null)
const resource = ref<Resource | null>(null)
const form = reactive({ title: '', folder: '', tags: [] as string[] })
const saving = ref(false)

const currentIndex = computed(() => {
  if (currentId.value === null) return -1
  return ids.value.indexOf(currentId.value)
})

const totalCount = computed(() => ids.value.length)

const resourceCache = new Map<number, Resource>()
const preloadedVideos = new Set<string>()

async function fetchIds() {
  ids.value = await $fetch<number[]>(`${apiBase}/resources/ids`, {
    query: { type: 'video' }
  })
}

async function fetchResource(id: number) {
  const cached = resourceCache.get(id)
  if (cached) {
    resource.value = cached
  }
  else {
    const data = await $fetch<Resource>(`${apiBase}/resources/${id}`)
    resourceCache.set(id, data)
    resource.value = data
  }
  form.title = resource.value.title ?? ''
  form.folder = resource.value.folder ?? ''
  form.tags = resource.value.tags.map(t => t.name)
}

function preloadVideo(res: Resource) {
  if (!res.url) return
  const fullUrl = `${apiBase}/media/${res.folder ? res.folder + '/' : ''}${res.url}`
  if (preloadedVideos.has(fullUrl)) return
  preloadedVideos.add(fullUrl)
  fetch(fullUrl).catch(() => {})
}

async function preloadResource(id: number) {
  if (!resourceCache.has(id)) {
    try {
      const data = await $fetch<Resource>(`${apiBase}/resources/${id}`)
      resourceCache.set(id, data)
    }
    catch { return }
  }
  preloadVideo(resourceCache.get(id)!)
}

function preloadAdjacent() {
  const idx = currentIndex.value
  for (const offset of [-2, -1, 1, 2]) {
    const adjIdx = idx + offset
    if (adjIdx >= 0 && adjIdx < ids.value.length) {
      preloadResource(ids.value[adjIdx])
    }
  }
}

function navigateTo(id: number) {
  currentId.value = id
  router.replace({ query: { id: String(id) } })
  fetchResource(id).then(() => preloadAdjacent())
}

function prev() {
  const idx = currentIndex.value
  if (idx > 0) navigateTo(ids.value[idx - 1])
}

function next() {
  const idx = currentIndex.value
  if (idx < ids.value.length - 1) navigateTo(ids.value[idx + 1])
}

function onKeydown(e: KeyboardEvent) {
  const tag = (e.target as HTMLElement)?.tagName
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return
  if (e.key === 'ArrowLeft') prev()
  else if (e.key === 'ArrowRight') next()
}

onMounted(async () => {
  window.addEventListener('keydown', onKeydown)
  await fetchIds()
  if (ids.value.length === 0) return
  const queryId = Number(route.query.id)
  const startId = queryId && ids.value.includes(queryId) ? queryId : ids.value[0]
  navigateTo(startId)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})

async function saveForm() {
  if (!currentId.value) return
  saving.value = true
  try {
    const updated = await $fetch<Resource>(`${apiBase}/resources/${currentId.value}`, {
      method: 'PUT',
      body: { title: form.title, folder: form.folder || null, tags: form.tags }
    })
    resource.value = updated
    resourceCache.set(currentId.value, updated)
  }
  finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <UBreadcrumb
      :items="[
        { label: 'Resources', to: '/resources' },
        { label: 'Videos', to: '/resources/videos' },
        { label: 'Viewer' }
      ]"
    />

    <div v-if="ids.length === 0" class="text-center text-gray-500 py-12">
      No videos found.
    </div>

    <div v-else-if="resource" class="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg min-h-[400px]">
          <video
            :key="resource.id"
            controls
            :src="apiBase + '/media/' + (resource.folder ? resource.folder + '/' : '') + resource.url"
            class="max-h-[70vh] max-w-full"
          />
        </div>

        <div class="flex items-center justify-center gap-4">
          <UButton icon="i-lucide-chevron-left" variant="outline" color="neutral" :disabled="currentIndex <= 0" @click="prev" />
          <span class="text-sm text-gray-500">{{ currentIndex + 1 }} / {{ totalCount }}</span>
          <UButton icon="i-lucide-chevron-right" variant="outline" color="neutral" :disabled="currentIndex >= ids.length - 1" @click="next" />
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-lg font-semibold truncate">
          {{ resource.title || 'Untitled' }}
        </h2>
        <UFormField label="Title" name="title">
          <UInput v-model="form.title" placeholder="Video title" class="w-full" />
        </UFormField>
        <UFormField label="Folder" name="folder">
          <UInput v-model="form.folder" placeholder="e.g. 2024/vacation" class="w-full" />
        </UFormField>
        <UFormField label="Tags" name="tags">
          <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
        </UFormField>
        <div>
          <UButton label="Save" :loading="saving" @click="saveForm" />
        </div>
      </div>
    </div>
  </div>
</template>
