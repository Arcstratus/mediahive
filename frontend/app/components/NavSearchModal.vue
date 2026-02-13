<script setup lang="ts">
import { allDomains } from '~/services/domains'

const open = ref(false)

// TODO: 後端支援 - 從 API 取得使用者可存取的頁面清單
const groups = allDomains.map(domain => ({
  id: domain.id,
  label: domain.label,
  items: domain.services.map(service => ({
    label: service.label,
    icon: service.icon,
    to: service.path,
  })),
}))

function onSelect(item: { to?: string }) {
  if (item.to) {
    open.value = false
    navigateTo(item.to)
  }
}
</script>

<template>
  <UModal v-model:open="open" :ui="{ width: 'sm:max-w-2xl' }">
    <UButton
      icon="i-lucide-search"
      variant="ghost"
      color="neutral"
      aria-label="搜尋"
    />

    <template #content>
      <UCommandPalette
        :groups="groups"
        placeholder="搜尋頁面..."
        class="h-80"
        @update:model-value="onSelect"
      />
    </template>
  </UModal>
</template>
