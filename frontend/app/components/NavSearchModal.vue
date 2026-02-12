<script setup lang="ts">
const open = ref(false)

// TODO: 後端支援 - 從 API 取得使用者可存取的頁面清單
const groups = [
  {
    id: 'modules',
    label: '模組',
    items: [
      { label: 'Foundation 基礎模組', icon: 'i-lucide-settings', to: '/foundation' },
      { label: 'ERP 企業資源規劃', icon: 'i-lucide-package', to: '/erp' },
      { label: 'HRM 人力資源管理', icon: 'i-lucide-users', to: '/hrm' },
      { label: 'CRM 客戶關係管理', icon: 'i-lucide-handshake', to: '/crm' },
    ],
  },
  {
    id: 'resources',
    label: '資源管理',
    items: [
      { label: '資源列表', icon: 'i-lucide-library', to: '/resources' },
      { label: '資源資料夾', icon: 'i-lucide-folders', to: '/resources/folders' },
      { label: '資源回收桶', icon: 'i-lucide-trash-2', to: '/resources/trash' },
    ],
  },
  {
    id: 'bookmarks',
    label: '書籤管理',
    items: [
      { label: '書籤列表', icon: 'i-lucide-bookmark', to: '/bookmarks' },
      { label: '書籤資料夾', icon: 'i-lucide-folders', to: '/bookmarks/folders' },
    ],
  },
  {
    id: 'tags',
    label: '標籤管理',
    items: [
      { label: '標籤列表', icon: 'i-lucide-tag', to: '/tags' },
    ],
  },
]

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
