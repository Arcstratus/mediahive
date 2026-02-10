<script setup lang="ts">
import type { FolderInfo } from '~/types'

definePageMeta({
  layout: 'dashboard'
})

const { public: { apiBase } } = useRuntimeConfig()

const { data: folders } = await useFetch<FolderInfo[]>(`${apiBase}/resources/folders`)

const search = ref('')

const filteredFolders = computed(() => {
  if (!folders.value) return []
  if (!search.value) return folders.value
  const q = search.value.toLowerCase()
  return folders.value.filter(f => f.folder.toLowerCase().includes(q))
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Folders' }]" />

    <UInput v-model="search" placeholder="Filter folders..." icon="i-lucide-search" class="max-w-sm" />

    <div v-if="filteredFolders.length === 0" class="text-center text-gray-500 py-12">
      No folders found.
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <UCard
        v-for="item in filteredFolders"
        :key="item.folder"
        class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition"
        @click="navigateTo(`/folders/viewer?folder=${encodeURIComponent(item.folder)}`)"
      >
        <div class="flex items-center gap-3">
          <UIcon name="i-lucide-folder" class="size-8 text-primary-500 shrink-0" />
          <div class="min-w-0">
            <p class="font-medium truncate">{{ item.folder }}</p>
            <p class="text-sm text-gray-500">{{ item.count }} resource{{ item.count === 1 ? '' : 's' }}</p>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>
