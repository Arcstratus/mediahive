<script setup lang="ts">
interface BreadcrumbItem {
  label: string
  icon?: string
  to?: string
}

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
