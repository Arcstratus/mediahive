<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Dashboard</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-film" class="size-5" />
            <h3 class="font-semibold">Media Files</h3>
          </div>
        </template>
        <p class="text-sm text-muted">0 items in library</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-hard-drive" class="size-5" />
            <h3 class="font-semibold">Storage</h3>
          </div>
        </template>
        <p class="text-sm text-muted">0 GB used</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-activity" class="size-5" />
            <h3 class="font-semibold">Recent Activity</h3>
          </div>
        </template>
        <p class="text-sm text-muted">No recent activity</p>
      </UCard>
    </div>
  </div>
</template>
