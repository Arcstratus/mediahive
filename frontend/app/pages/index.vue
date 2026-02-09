<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})

interface Tag {
  id: number
  name: string
  created_at: string
  resource_count: number
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

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

interface Stats {
  images: number
  videos: number
  urls: number
  tags: number
}

interface ScannedFile {
  path: string
  name: string
  type: 'image' | 'video'
  size: number
}

const { public: { apiBase } } = useRuntimeConfig()

const { data: stats, refresh: refreshStats } = await useAsyncData<Stats>('dashboard-stats', () =>
  $fetch(`${apiBase}/stats`)
)

const { data: recentData, refresh: refreshRecent } = await useAsyncData<PaginatedResponse>('dashboard-recent', () =>
  $fetch(`${apiBase}/resources`, {
    query: { sort_by: 'created_at', sort_desc: true, per_page: 8 }
  })
)

const { data: tags, refresh: refreshTags } = await useAsyncData<Tag[]>('dashboard-tags', () =>
  $fetch(`${apiBase}/tags`)
)

const recentResources = computed(() => recentData.value?.items ?? [])

const statCards = computed(() => [
  { label: 'Images', icon: 'i-lucide-image', count: stats.value?.images ?? 0, to: '/resources/images' },
  { label: 'Videos', icon: 'i-lucide-video', count: stats.value?.videos ?? 0, to: '/resources/videos' },
  { label: 'URLs', icon: 'i-lucide-link', count: stats.value?.urls ?? 0, to: '/resources/urls' },
  { label: 'Tags', icon: 'i-lucide-tags', count: stats.value?.tags ?? 0, to: '/tags' },
])

// Tag cloud sizing
const TAG_SIZES = ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl']

function getTagSize(count: number, min: number, max: number): string {
  if (min === max) return TAG_SIZES[3]
  const index = Math.round(((count - min) / (max - min)) * (TAG_SIZES.length - 1))
  return TAG_SIZES[index]
}

const tagCloud = computed(() => {
  const allTags = tags.value ?? []
  if (!allTags.length) return []
  const counts = allTags.map(t => t.resource_count)
  const min = Math.min(...counts)
  const max = Math.max(...counts)
  return allTags.map(t => ({
    ...t,
    sizeClass: getTagSize(t.resource_count, min, max),
  }))
})

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

function getMediaUrl(resource: Resource): string {
  if (!resource.url) return ''
  const folder = resource.folder ? `${resource.folder}/` : ''
  return `${apiBase}/media/${folder}${resource.url}`
}

// Upload modal
const uploadOpen = ref(false)
const uploadFile = ref<File | null>(null)
const uploadForm = reactive({ title: '', tags: [] as string[] })
const uploading = ref(false)

function openUpload() {
  uploadFile.value = null
  uploadForm.title = ''
  uploadForm.tags = []
  uploading.value = false
  uploadOpen.value = true
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  uploadFile.value = input.files?.[0] ?? null
}

async function submitUpload() {
  if (!uploadFile.value) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    if (uploadForm.title) formData.append('title', uploadForm.title)
    if (uploadForm.tags.length) formData.append('tags', uploadForm.tags.join(','))
    await $fetch(`${apiBase}/resources/upload`, {
      method: 'POST',
      body: formData,
    })
    uploadOpen.value = false
    await Promise.all([refreshStats(), refreshRecent(), refreshTags()])
  }
  finally {
    uploading.value = false
  }
}

// Import folder modal
const importOpen = ref(false)
const folderPath = ref('')
const scannedFiles = ref<ScannedFile[]>([])
const scanned = ref(false)
const scanning = ref(false)
const importing = ref(false)
const importResult = ref<{ imported: number; skipped: number } | null>(null)

function resetImport() {
  folderPath.value = ''
  scannedFiles.value = []
  scanned.value = false
  importResult.value = null
  scanning.value = false
  importing.value = false
}

async function scanFolder() {
  scanning.value = true
  try {
    const res = await $fetch<{ files: ScannedFile[] }>(`${apiBase}/imports/scan`, {
      method: 'POST',
      body: { path: folderPath.value },
    })
    scannedFiles.value = res.files
    scanned.value = true
  }
  catch (err) {
    console.error('Scan failed:', err)
  }
  finally {
    scanning.value = false
  }
}

async function executeImport() {
  importing.value = true
  try {
    const res = await $fetch<{ imported: number; skipped: number }>(`${apiBase}/imports/execute`, {
      method: 'POST',
      body: {
        files: scannedFiles.value.map(f => ({ path: f.path, type: f.type })),
      },
    })
    importResult.value = res
    await Promise.all([refreshStats(), refreshRecent(), refreshTags()])
  }
  catch (err) {
    console.error('Import failed:', err)
  }
  finally {
    importing.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Dashboard</h1>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <NuxtLink v-for="card in statCards" :key="card.label" :to="card.to">
        <UCard class="hover:ring-1 hover:ring-primary transition">
          <div class="flex items-center gap-3">
            <UIcon :name="card.icon" class="size-8 text-primary" />
            <div>
              <p class="text-3xl font-bold">{{ card.count }}</p>
              <p class="text-sm text-muted">{{ card.label }}</p>
            </div>
          </div>
        </UCard>
      </NuxtLink>
    </div>

    <!-- Recently Added + Quick Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recently Added -->
      <div class="lg:col-span-2">
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="font-semibold">Recently Added</h2>
              <UButton label="View All" variant="ghost" to="/resources" size="sm" />
            </div>
          </template>
          <div v-if="recentResources.length" class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <NuxtLink
              v-for="resource in recentResources"
              :key="resource.id"
              :to="resource.type === 'url' ? undefined : `/resources/${resource.type === 'image' ? 'images' : 'videos'}/viewer?id=${resource.id}`"
              class="group flex flex-col gap-1"
            >
              <div class="aspect-square rounded-lg bg-elevated overflow-hidden flex items-center justify-center">
                <img
                  v-if="resource.type === 'image' && resource.url"
                  :src="getMediaUrl(resource)"
                  :alt="resource.title ?? ''"
                  class="size-full object-cover group-hover:scale-105 transition"
                >
                <UIcon
                  v-else-if="resource.type === 'video'"
                  name="i-lucide-video"
                  class="size-10 text-muted"
                />
                <UIcon
                  v-else
                  name="i-lucide-link"
                  class="size-10 text-muted"
                />
              </div>
              <p class="text-xs truncate" :title="resource.title ?? ''">{{ resource.title ?? 'Untitled' }}</p>
              <p class="text-xs text-muted">{{ formatDate(resource.created_at) }}</p>
            </NuxtLink>
          </div>
          <p v-else class="text-sm text-muted">No resources yet.</p>
        </UCard>
      </div>

      <!-- Quick Actions -->
      <div>
        <UCard>
          <template #header>
            <h2 class="font-semibold">Quick Actions</h2>
          </template>
          <div class="flex flex-col gap-2">
            <UButton
              label="Upload File"
              icon="i-lucide-upload"
              variant="soft"
              block
              @click="openUpload()"
            />
            <UButton
              label="Add URL"
              icon="i-lucide-link"
              variant="soft"
              block
              to="/resources/urls"
            />
            <UButton
              label="Import Folder"
              icon="i-lucide-folder-input"
              variant="soft"
              block
              @click="resetImport(); importOpen = true"
            />
          </div>
        </UCard>
      </div>
    </div>

    <!-- Tag Cloud -->
    <UCard v-if="tagCloud.length">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="font-semibold">Tags</h2>
          <UButton label="Manage Tags" variant="ghost" to="/tags" size="sm" />
        </div>
      </template>
      <div class="flex flex-wrap gap-3 items-baseline">
        <NuxtLink
          v-for="tag in tagCloud"
          :key="tag.id"
          :to="`/resources?tag=${encodeURIComponent(tag.name)}`"
          :class="[tag.sizeClass, 'text-muted hover:text-primary transition-colors']"
          :title="`${tag.name} (${tag.resource_count})`"
        >
          {{ tag.name }}
        </NuxtLink>
      </div>
    </UCard>

    <!-- Upload Modal -->
    <UModal v-model:open="uploadOpen" title="Upload File">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="File" name="file">
            <input
              type="file"
              accept="image/*,video/*"
              @change="onFileChange"
            >
          </UFormField>
          <UFormField label="Title" name="title">
            <UInput v-model="uploadForm.title" placeholder="Title (optional)" class="w-full" />
          </UFormField>
          <UFormField label="Tags" name="tags">
            <UInputTags v-model="uploadForm.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
          </UFormField>
        </div>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Upload" :loading="uploading" :disabled="!uploadFile" @click="submitUpload" />
        </div>
      </template>
    </UModal>

    <!-- Import Folder Modal -->
    <UModal v-model:open="importOpen" title="Import Folder" :ui="{ width: 'sm:max-w-4xl' }">
      <template #body>
        <div v-if="importResult" class="flex flex-col gap-4">
          <p>
            Imported <strong>{{ importResult.imported }}</strong> file(s),
            skipped <strong>{{ importResult.skipped }}</strong> duplicate(s).
          </p>
        </div>
        <div v-else class="flex flex-col gap-4">
          <div class="flex gap-2">
            <UInput
              v-model="folderPath"
              placeholder="/path/to/folder"
              class="flex-1"
              :disabled="scanning"
            />
            <UButton
              label="Scan"
              :loading="scanning"
              :disabled="!folderPath.trim()"
              @click="scanFolder"
            />
          </div>
          <p v-if="scannedFiles.length > 0" class="text-sm text-muted">
            Found {{ scannedFiles.length }} file(s).
          </p>
          <p v-else-if="scanned" class="text-sm text-muted">
            No image or video files found in this folder.
          </p>
        </div>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Close" variant="outline" @click="close" />
          <UButton
            v-if="!importResult && scannedFiles.length > 0"
            label="Import"
            :loading="importing"
            @click="executeImport"
          />
        </div>
      </template>
    </UModal>
  </div>
</template>
