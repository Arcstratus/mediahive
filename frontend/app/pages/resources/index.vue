<script setup lang="ts">
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

const { data } = await useAsyncData<PaginatedResponse>('all-resources', () =>
  $fetch(`${apiBase}/resources`, { query: { per_page: 100 } })
)

const items = computed(() => data.value?.items ?? [])
const urlCount = computed(() => items.value.filter(r => r.type === 'url').length)
const imageCount = computed(() => items.value.filter(r => r.type === 'image').length)
const videoCount = computed(() => items.value.filter(r => r.type === 'video').length)

const cards = [
  { label: 'URLs', icon: 'i-lucide-link', to: '/resources/urls', count: urlCount },
  { label: 'Images', icon: 'i-lucide-image', to: '/resources/images', count: imageCount },
  { label: 'Videos', icon: 'i-lucide-video', to: '/resources/videos', count: videoCount }
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Resources</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <NuxtLink v-for="card in cards" :key="card.label" :to="card.to">
        <UCard class="hover:ring-1 hover:ring-primary transition">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon :name="card.icon" class="size-5" />
              <h3 class="font-semibold">{{ card.label }}</h3>
            </div>
          </template>
          <p class="text-3xl font-bold">{{ card.count.value }}</p>
          <p class="text-sm text-muted">items</p>
        </UCard>
      </NuxtLink>
    </div>
  </div>
</template>
