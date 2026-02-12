<script setup lang="ts">
const route = useRoute()

const modules = [
  { label: 'Foundation', icon: 'i-lucide-settings', path: '/foundation' },
  { label: 'ERP', icon: 'i-lucide-package', path: '/erp' },
  { label: 'HRM', icon: 'i-lucide-users', path: '/hrm' },
  { label: 'CRM', icon: 'i-lucide-handshake', path: '/crm' },
]

const currentModule = computed(() => {
  const path = route.path
  return modules.find(m => path.startsWith(m.path))
})

const currentModuleLabel = computed(() => currentModule.value?.label ?? 'Mediahive')

const moduleMenuItems = computed(() => [
  modules.map(m => ({
    label: m.label,
    icon: m.icon,
    onSelect() {
      navigateTo(m.path)
    },
  })),
])

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
        <UDashboardNavbar>
          <template #leading>
            <UDashboardSidebarCollapse />
          </template>

          <template #left>
            <UDropdownMenu :items="moduleMenuItems">
              <UButton
                :icon="currentModule?.icon ?? 'i-lucide-layout-grid'"
                :label="currentModuleLabel"
                trailing-icon="i-lucide-chevron-down"
                variant="outline"
                color="neutral"
              />
            </UDropdownMenu>
          </template>

          <template #right>
            <NavSearchModal />
            <NavNotifications />
            <NavSettingsDrawer />
            <NavUserMenu />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <slot />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
