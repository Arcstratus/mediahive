<script setup lang="ts">
import type { Resource } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const { public: { apiBase } } = useRuntimeConfig()
const resourcesApi = useResourcesApi()
const toast = useToast()
const { confirm } = useConfirmDialog()
const route = useRoute()
const router = useRouter()

const ids = ref<number[]>([])
const currentId = ref<number | null>(null)
const resource = ref<Resource | null>(null)
const form = reactive({ title: '', folder: '', tags: [] as string[] })
const saving = ref(false)
const videoRef = ref<HTMLVideoElement | null>(null)
const settingThumbnail = ref(false)

const currentIndex = computed(() => {
  if (currentId.value === null) return -1
  return ids.value.indexOf(currentId.value)
})

const totalCount = computed(() => ids.value.length)

const resourceCache = new Map<number, Resource>()
const imageCache = new Map<string, HTMLImageElement>()
const preloadedVideos = new Set<string>()

async function fetchIds() {
  const { data } = await resourcesApi.getIds()
  if (data) ids.value = data
}

async function fetchResource(id: number) {
  const cached = resourceCache.get(id)
  if (cached) {
    resource.value = cached
  }
  else {
    const { data } = await resourcesApi.get(id)
    if (!data) return
    resourceCache.set(id, data)
    resource.value = data
  }
  form.title = resource.value.title ?? ''
  form.folder = resource.value.folder ?? ''
  form.tags = resource.value.tags.map(t => t.name)
}

function preloadMedia(res: Resource) {
  if (!res.filename) return
  const folder = res.folder ? `${res.folder}/` : ''
  const fullUrl = `${apiBase}/media/${folder}${res.filename}`
  if (res.category === 'image') {
    if (imageCache.has(fullUrl)) return
    const img = new Image()
    img.src = fullUrl
    imageCache.set(fullUrl, img)
  }
  else {
    if (preloadedVideos.has(fullUrl)) return
    preloadedVideos.add(fullUrl)
    fetch(fullUrl).catch(() => {})
  }
}

async function preloadResource(id: number) {
  if (!resourceCache.has(id)) {
    const { data } = await resourcesApi.get(id)
    if (!data) return
    resourceCache.set(id, data)
  }
  preloadMedia(resourceCache.get(id)!)
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

function navigateToId(id: number) {
  currentId.value = id
  router.replace({ query: { id: String(id) } })
  fetchResource(id).then(() => preloadAdjacent())
}

function prev() {
  const idx = currentIndex.value
  if (idx > 0) navigateToId(ids.value[idx - 1])
}

function next() {
  const idx = currentIndex.value
  if (idx < ids.value.length - 1) navigateToId(ids.value[idx + 1])
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
  navigateToId(startId)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})

async function deleteResource() {
  if (!currentId.value) return
  if (!await confirm({ message: 'Are you sure you want to delete this resource?' })) return
  const { error } = await resourcesApi.remove(currentId.value)
  if (error) { toast.add({ title: error, color: 'error' }); return }
  const idx = currentIndex.value
  ids.value.splice(idx, 1)
  resourceCache.delete(currentId.value)
  if (ids.value.length === 0) {
    router.replace('/resources')
    return
  }
  const nextId = ids.value[Math.min(idx, ids.value.length - 1)]
  navigateToId(nextId)
}

async function saveForm() {
  if (!currentId.value) return
  saving.value = true
  const { data: updated, error } = await resourcesApi.update(currentId.value, { title: form.title, folder: form.folder || null, tags: form.tags })
  saving.value = false
  if (error) { toast.add({ title: error, color: 'error' }); return }
  resource.value = updated
  resourceCache.set(currentId.value, updated)
}

async function setThumbnail() {
  if (!currentId.value || !videoRef.value) return
  settingThumbnail.value = true
  const { data: updated, error } = await resourcesApi.setThumbnail(currentId.value, videoRef.value.currentTime)
  settingThumbnail.value = false
  if (error) { toast.add({ title: error, color: 'error' }); return }
  resource.value = updated
  resourceCache.set(currentId.value, updated)
}

async function removeThumbnail() {
  if (!currentId.value) return
  settingThumbnail.value = true
  const { data: updated, error } = await resourcesApi.removeThumbnail(currentId.value)
  settingThumbnail.value = false
  if (error) { toast.add({ title: error, color: 'error' }); return }
  resource.value = updated
  resourceCache.set(currentId.value, updated)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb
      :items="[
        { label: 'Resources', to: '/resources' },
        { label: 'Viewer' }
      ]"
    />

    <div v-if="ids.length === 0" class="text-center text-gray-500 py-12">
      No resources found.
    </div>

    <div v-else-if="resource" class="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg min-h-[400px]">
          <img
            v-if="resource.category === 'image'"
            :src="`${apiBase}/media/${resource.folder ? resource.folder + '/' : ''}${resource.filename}`"
            :alt="resource.title ?? ''"
            class="max-h-[70vh] max-w-full object-contain"
          >
          <video
            v-else
            ref="videoRef"
            :key="resource.id"
            controls
            :poster="resource.thumbnail ? `${apiBase}/thumbnails/${resource.thumbnail}` : undefined"
            :src="`${apiBase}/media/${resource.folder ? resource.folder + '/' : ''}${resource.filename}`"
            class="max-h-[70vh] max-w-full"
          />
        </div>

        <div class="flex items-center justify-center gap-4">
          <UButton icon="i-lucide-chevron-left" variant="outline" color="neutral" :disabled="currentIndex <= 0" @click="prev" />
          <span class="text-sm text-gray-500">{{ currentIndex + 1 }} / {{ totalCount }}</span>
          <UButton icon="i-lucide-chevron-right" variant="outline" color="neutral" :disabled="currentIndex >= ids.length - 1" @click="next" />
        </div>

        <div v-if="resource.category === 'video'" class="flex items-center justify-center">
          <UButton label="Set as Thumbnail" icon="i-lucide-camera" variant="soft" :loading="settingThumbnail" @click="setThumbnail" />
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-lg font-semibold truncate">
          {{ resource.title || 'Untitled' }}
        </h2>
        <UBadge :label="resource.category" :color="resource.category === 'image' ? 'info' : 'warning'" variant="subtle" size="sm" class="w-fit" />
        <div v-if="resource.thumbnail" class="flex flex-col gap-2">
          <p class="text-sm font-medium text-muted">Thumbnail</p>
          <img :src="`${apiBase}/thumbnails/${resource.thumbnail}`" alt="Thumbnail" class="rounded-lg w-full object-cover" >
          <UButton label="Remove Thumbnail" icon="i-lucide-x" variant="soft" color="error" size="sm" :loading="settingThumbnail" @click="removeThumbnail" />
        </div>
        <UFormField label="Title" name="title">
          <UInput v-model="form.title" placeholder="Title" class="w-full" />
        </UFormField>
        <UFormField label="Folder" name="folder">
          <UInput v-model="form.folder" placeholder="e.g. 2024/vacation" class="w-full" />
        </UFormField>
        <UFormField label="Tags" name="tags">
          <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
        </UFormField>
        <div class="flex gap-2">
          <UButton label="Save" :loading="saving" @click="saveForm" />
          <UButton label="Delete" icon="i-lucide-trash-2" color="error" variant="soft" @click="deleteResource" />
        </div>
      </div>
    </div>
  </div>
</template>
