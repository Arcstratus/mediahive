<script setup lang="ts">
const { currentDomain, sidebarItems, domainMenuItems } = useServiceRegistry()

const currentDomainLabel = computed(() => currentDomain.value?.label ?? 'Mediahive')
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
          :items="sidebarItems"
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
            <UDropdownMenu :items="domainMenuItems">
              <UButton
                :icon="currentDomain?.icon ?? 'i-lucide-layout-grid'"
                :label="currentDomainLabel"
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
