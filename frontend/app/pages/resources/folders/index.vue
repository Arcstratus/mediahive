<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})

const resourcesApi = useResourcesApi()

const { data: folders } = await resourcesApi.getFolders('resource-folders')
const { treeItems } = useFolderTree(folders)

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
    <PageBreadcrumb :items="[{ label: 'Resources', to: '/resources' }, { label: 'Folders' }]" />

    <div class="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6">
      <!-- Left panel: folder tree -->
      <div class="hidden lg:block">
        <ClientOnly>
          <UTree
            v-if="treeItems.length"
            :items="treeItems"
            collapsed-icon="i-lucide-folder"
            expanded-icon="i-lucide-folder-open"
          >
            <template #item="{ item }">
              <NuxtLink
                :to="`/resources/folders/${item.value?.path}`"
                class="flex items-center gap-2 w-full hover:text-primary truncate"
              >
                <span class="truncate">{{ item.label }}</span>
                <span v-if="item.value?.count" class="text-xs text-muted">({{ item.value.count }})</span>
              </NuxtLink>
            </template>
          </UTree>
          <p v-else class="text-sm text-muted">No folders yet.</p>
        </ClientOnly>
      </div>

      <!-- Right panel: folder cards -->
      <div class="flex flex-col gap-4">
        <UInput v-model="search" placeholder="Filter folders..." icon="i-lucide-search" class="max-w-sm" />

        <div v-if="filteredFolders.length === 0" class="text-center text-gray-500 py-12">
          No folders found.
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <UCard
            v-for="item in filteredFolders"
            :key="item.folder"
            class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition"
            @click="navigateTo(`/resources/folders/${encodeURIComponent(item.folder)}`)"
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
    </div>
  </div>
</template>
