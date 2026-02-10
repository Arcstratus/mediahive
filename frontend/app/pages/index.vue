<script setup lang="ts">
import type { Tag, Resource, PaginatedResponse, Stats } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

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
  { label: 'Images', icon: 'i-lucide-image', count: stats.value?.images ?? 0, to: '/resources' },
  { label: 'Videos', icon: 'i-lucide-video', count: stats.value?.videos ?? 0, to: '/resources' },
  { label: 'Bookmarks', icon: 'i-lucide-bookmark', count: stats.value?.bookmarks ?? 0, to: '/bookmarks' },
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
  if (!resource.filename) return ''
  const folder = resource.folder ? `${resource.folder}/` : ''
  return `${apiBase}/media/${folder}${resource.filename}`
}

function getThumbnailUrl(resource: Resource): string {
  if (!resource.thumbnail) return ''
  return `${apiBase}/thumbnails/${resource.thumbnail}`
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

// Bookmark modal
const bookmarkOpen = ref(false)

async function onBookmarkSaved() {
  await Promise.all([refreshStats(), refreshRecent(), refreshTags()])
}

// Stream player modal
const streamOpen = ref(false)

// Import folder modal
const importOpen = ref(false)

async function onImported() {
  await Promise.all([refreshStats(), refreshRecent(), refreshTags()])
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
              :to="`/resources/viewer?id=${resource.id}`"
              class="group flex flex-col gap-1"
            >
              <div class="aspect-square rounded-lg bg-elevated overflow-hidden flex items-center justify-center">
                <img
                  v-if="resource.category === 'image' && resource.filename"
                  :src="getMediaUrl(resource)"
                  :alt="resource.title ?? ''"
                  class="size-full object-cover group-hover:scale-105 transition"
                >
                <img
                  v-else-if="resource.thumbnail"
                  :src="getThumbnailUrl(resource)"
                  :alt="resource.title ?? ''"
                  class="size-full object-cover group-hover:scale-105 transition"
                >
                <UIcon
                  v-else
                  name="i-lucide-video"
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
              label="Add Bookmark"
              icon="i-lucide-bookmark"
              variant="soft"
              block
              @click="bookmarkOpen = true"
            />
            <UButton
              label="Import Folder"
              icon="i-lucide-folder-input"
              variant="soft"
              block
              @click="importOpen = true"
            />
            <UButton
              label="Play Stream"
              icon="i-lucide-play"
              variant="soft"
              block
              @click="streamOpen = true"
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

    <!-- Bookmark Modal -->
    <BookmarkModal v-model:open="bookmarkOpen" @saved="onBookmarkSaved" />

    <!-- Stream Player Modal -->
    <M3u8PlayerModal v-model:open="streamOpen" />

    <!-- Import Folder Modal -->
    <ImportFolderModal v-model:open="importOpen" @imported="onImported" />
  </div>
</template>
