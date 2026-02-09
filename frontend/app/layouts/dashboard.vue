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
    label: 'Image Viewer',
    icon: 'i-lucide-image',
    to: '/resources/images/viewer'
  },
  {
    label: 'Video Viewer',
    icon: 'i-lucide-clapperboard',
    to: '/resources/videos/viewer'
  },
  {
    label: 'Tags',
    icon: 'i-lucide-tag',
    to: '/tags'
  },
  {
    label: 'Settings',
    icon: 'i-lucide-settings',
    to: '/settings'
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
