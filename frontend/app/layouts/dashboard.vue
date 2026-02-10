<script setup lang="ts">
const items = [
  {
    label: 'Home',
    icon: 'i-lucide-house',
    to: '/'
  },
  {
    label: 'Resources',
    icon: 'i-lucide-library',
    to: '/resources'
  },
  {
    label: 'Folders',
    icon: 'i-lucide-folders',
    to: '/folders'
  },
  {
    label: 'Bookmarks',
    icon: 'i-lucide-bookmark',
    to: '/bookmarks'
  },
  {
    label: 'Tags',
    icon: 'i-lucide-tag',
    to: '/tags'
  },
  {
    label: 'Trash',
    icon: 'i-lucide-trash-2',
    to: '/trash'
  }
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
