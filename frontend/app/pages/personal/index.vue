<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const features = [
  { title: '資源管理', description: '管理圖片、影片等多媒體資源', icon: 'i-lucide-library', to: '/resources' },
  { title: '書籤管理', description: '收藏與整理網路書籤', icon: 'i-lucide-bookmark', to: '/bookmarks' },
  { title: '標籤管理', description: '建立與管理分類標籤', icon: 'i-lucide-tag', to: '/tags' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Personal' }]" />

    <h1 class="text-2xl font-bold">Personal 個人資源</h1>
    <p class="text-muted">管理個人的多媒體資源、書籤與標籤。</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <NuxtLink v-for="feature in features" :key="feature.title" :to="feature.to">
        <UCard class="h-full hover:ring-primary/50 hover:ring-1 transition-all cursor-pointer">
          <div class="flex items-start gap-3">
            <UIcon :name="feature.icon" class="size-8 text-primary shrink-0 mt-0.5" />
            <div>
              <h3 class="font-semibold">{{ feature.title }}</h3>
              <p class="text-sm text-muted mt-1">{{ feature.description }}</p>
            </div>
          </div>
        </UCard>
      </NuxtLink>
    </div>
  </div>
</template>
