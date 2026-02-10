<script setup lang="ts">
import type { Tag } from '~/types'

const props = defineProps<{
  tags: Tag[]
}>()

const TAG_SIZES = ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl']

function getTagSize(count: number, min: number, max: number): string {
  if (min === max) return TAG_SIZES[3]
  const index = Math.round(((count - min) / (max - min)) * (TAG_SIZES.length - 1))
  return TAG_SIZES[index]
}

const tagCloud = computed(() => {
  if (!props.tags.length) return []
  const counts = props.tags.map(t => t.resource_count ?? 0)
  const min = Math.min(...counts)
  const max = Math.max(...counts)
  return props.tags.map(t => ({
    ...t,
    sizeClass: getTagSize(t.resource_count ?? 0, min, max),
  }))
})
</script>

<template>
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
</template>
