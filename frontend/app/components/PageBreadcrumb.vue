<script setup lang="ts">
import type { BreadcrumbItem } from '~/types'

const props = defineProps<{
  items: BreadcrumbItem[]
}>()

const allItems = computed(() => [
  { label: 'Home', icon: 'i-lucide-house', to: '/' },
  ...props.items
])
</script>

<template>
  <UBreadcrumb :items="allItems" />
</template>
