<script setup lang="ts">
const items = [
  {
    label: 'Home',
    icon: 'i-lucide-house',
    to: '/'
  },
  {
    label: 'Library',
    icon: 'i-lucide-library',
    to: '/library'
  },
  {
    label: 'Upload',
    icon: 'i-lucide-upload',
    to: '/upload'
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
