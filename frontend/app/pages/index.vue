<script setup lang="ts">

definePageMeta({
  layout: 'dashboard'
})

const resourcesApi = useResourcesApi()
const tagsApi = useTagsApi()
const statsApi = useStatsApi()

const { data: stats, refresh: refreshStats } = await statsApi.get('dashboard-stats')

const { data: recentData, refresh: refreshRecent } = await resourcesApi.list('dashboard-recent', { sort_by: 'created_at', sort_desc: true, per_page: 8 })

const { data: tags, refresh: refreshTags } = await tagsApi.list('dashboard-tags')

const recentResources = computed(() => recentData.value?.items ?? [])

const statCards = computed(() => [
  { label: 'Images', icon: 'i-lucide-image', count: stats.value?.images ?? 0, to: '/resources' },
  { label: 'Videos', icon: 'i-lucide-video', count: stats.value?.videos ?? 0, to: '/resources' },
  { label: 'Bookmarks', icon: 'i-lucide-bookmark', count: stats.value?.bookmarks ?? 0, to: '/bookmarks' },
  { label: 'Tags', icon: 'i-lucide-tags', count: stats.value?.tags ?? 0, to: '/tags' },
])

const { public: { apiBase } } = useRuntimeConfig()

// Modal states
const uploadOpen = ref(false)
const bookmarkOpen = ref(false)
const importBookmarksOpen = ref(false)
const importOpen = ref(false)

async function onRefreshAll() {
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
                  :src="`${apiBase}/media/${resource.folder ? resource.folder + '/' : ''}${resource.filename}`"
                  :alt="resource.title ?? ''"
                  class="size-full object-cover group-hover:scale-105 transition"
                >
                <img
                  v-else-if="resource.thumbnail"
                  :src="`${apiBase}/thumbnails/${resource.thumbnail}`"
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
              @click="uploadOpen = true"
            />
            <UButton
              label="Add Bookmark"
              icon="i-lucide-bookmark"
              variant="soft"
              block
              @click="bookmarkOpen = true"
            />
            <UButton
              label="Import Bookmarks"
              icon="i-lucide-file-down"
              variant="soft"
              block
              @click="importBookmarksOpen = true"
            />
            <UButton
              label="Import Folder"
              icon="i-lucide-folder-input"
              variant="soft"
              block
              @click="importOpen = true"
            />
          </div>
        </UCard>
      </div>
    </div>

    <!-- Tag Cloud -->
    <TagCloud :tags="tags ?? []" />

    <UploadModal v-model:open="uploadOpen" @uploaded="onRefreshAll" />
    <BookmarkModal v-model:open="bookmarkOpen" @saved="onRefreshAll" />
    <ImportBookmarksModal v-model:open="importBookmarksOpen" @imported="onRefreshAll" />
    <ImportFolderModal v-model:open="importOpen" @imported="onRefreshAll" />
  </div>
</template>
