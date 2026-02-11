<script setup lang="ts">
const items = [
  {
    label: 'Home',
    icon: 'i-lucide-house',
    to: '/',
  },
  {
    label: 'Resources',
    icon: 'i-lucide-library',
    defaultOpen: true,
    children: [
      { label: 'List', icon: 'i-lucide-list', to: '/resources' },
      { label: 'Folders', icon: 'i-lucide-folders', to: '/resources/folders' },
      { label: 'Trash', icon: 'i-lucide-trash-2', to: '/resources/trash' },
    ],
  },
  {
    label: 'Bookmarks',
    icon: 'i-lucide-bookmark',
    defaultOpen: true,
    children: [
      { label: 'List', icon: 'i-lucide-list', to: '/bookmarks' },
      { label: 'Folders', icon: 'i-lucide-folders', to: '/bookmarks/folders' },
    ],
  },
  {
    label: 'Tags',
    icon: 'i-lucide-tag',
    defaultOpen: true,
    children: [
      { label: 'List', icon: 'i-lucide-list', to: '/tags' },
    ],
  },
]
</script>

<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible>
      <template #header="{ collapsed }">
        <span v-if="!collapsed" class="text-lg font-bold truncate">Mediahive</span>
        <UIcon v-else name="i-lucide-video" class="size-6" />
      </template>

      <template #default="{ collapsed }">
        <UNavigationMenu
          :items="items"
          orientation="vertical"
          :collapsed="collapsed"
        />
      </template>
    </UDashboardSidebar>

    <UDashboardPanel>
      <template #header>
        <UDashboardNavbar title="Mediahive">
          <template #leading>
            <UDashboardSidebarCollapse />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <slot />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
