<script setup lang="ts">
const route = useRoute()

const modules = [
  { label: 'Personal', icon: 'i-lucide-library', path: '/personal', prefixes: ['/personal', '/resources', '/bookmarks', '/tags'] },
  { label: 'Foundation', icon: 'i-lucide-settings', path: '/foundation', prefixes: ['/foundation'] },
  { label: 'ERP', icon: 'i-lucide-package', path: '/erp', prefixes: ['/erp'] },
  { label: 'HRM', icon: 'i-lucide-users', path: '/hrm', prefixes: ['/hrm'] },
  { label: 'CRM', icon: 'i-lucide-handshake', path: '/crm', prefixes: ['/crm'] },
]

const currentModule = computed(() => {
  const path = route.path
  return modules.find(m => m.prefixes.some(p => path.startsWith(p)))
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

const personalItems = [
  { label: '總覽', icon: 'i-lucide-layout-dashboard', to: '/personal' },
  {
    label: '資源管理',
    icon: 'i-lucide-library',
    defaultOpen: true,
    children: [
      { label: '資源列表', icon: 'i-lucide-list', to: '/resources' },
      { label: '資料夾', icon: 'i-lucide-folders', to: '/resources/folders' },
      { label: '回收桶', icon: 'i-lucide-trash-2', to: '/resources/trash' },
    ],
  },
  {
    label: '書籤管理',
    icon: 'i-lucide-bookmark',
    defaultOpen: true,
    children: [
      { label: '書籤列表', icon: 'i-lucide-list', to: '/bookmarks' },
      { label: '資料夾', icon: 'i-lucide-folders', to: '/bookmarks/folders' },
    ],
  },
  {
    label: '標籤管理',
    icon: 'i-lucide-tag',
    children: [
      { label: '標籤列表', icon: 'i-lucide-list', to: '/tags' },
    ],
  },
]

const foundationItems = [
  { label: '總覽', icon: 'i-lucide-layout-dashboard', to: '/foundation' },
  {
    label: '使用者管理',
    icon: 'i-lucide-users',
    defaultOpen: true,
    children: [
      { label: '使用者列表', icon: 'i-lucide-list', to: '/foundation/user' },
      { label: '新增使用者', icon: 'i-lucide-plus', to: '/foundation/user/new' },
    ],
  },
  {
    label: '組織架構',
    icon: 'i-lucide-building',
    defaultOpen: true,
    children: [
      { label: '部門列表', icon: 'i-lucide-list', to: '/foundation/department' },
      { label: '新增部門', icon: 'i-lucide-plus', to: '/foundation/department/new' },
    ],
  },
  {
    label: '角色權限',
    icon: 'i-lucide-shield',
    defaultOpen: true,
    children: [
      { label: '角色列表', icon: 'i-lucide-list', to: '/foundation/role' },
      { label: '新增角色', icon: 'i-lucide-plus', to: '/foundation/role/new' },
    ],
  },
  { label: '系統設定', icon: 'i-lucide-settings', to: '/foundation/settings' },
  { label: '通知中心', icon: 'i-lucide-bell', to: '/foundation/notification' },
  { label: '稽核日誌', icon: 'i-lucide-scroll-text', to: '/foundation/audit-log' },
  { label: '個人資料', icon: 'i-lucide-user', to: '/foundation/profile' },
]

const erpItems = [
  { label: '總覽', icon: 'i-lucide-layout-dashboard', to: '/erp' },
  { label: '庫存管理', icon: 'i-lucide-warehouse', to: '/erp/inventory' },
  { label: '採購管理', icon: 'i-lucide-shopping-cart', to: '/erp/purchase' },
  { label: '銷售管理', icon: 'i-lucide-receipt', to: '/erp/sales' },
  { label: '財務會計', icon: 'i-lucide-calculator', to: '/erp/finance' },
  { label: '生產製造', icon: 'i-lucide-factory', to: '/erp/production' },
  { label: '物流配送', icon: 'i-lucide-truck', to: '/erp/logistics' },
]

const hrmItems = [
  { label: '總覽', icon: 'i-lucide-layout-dashboard', to: '/hrm' },
  {
    label: '員工管理',
    icon: 'i-lucide-user',
    defaultOpen: true,
    children: [
      { label: '員工列表', icon: 'i-lucide-list', to: '/hrm/employee' },
      { label: '新增員工', icon: 'i-lucide-plus', to: '/hrm/employee/new' },
    ],
  },
  { label: '出勤管理', icon: 'i-lucide-clock', to: '/hrm/attendance' },
  { label: '薪資管理', icon: 'i-lucide-banknote', to: '/hrm/payroll' },
  { label: '績效考核', icon: 'i-lucide-trophy', to: '/hrm/performance' },
  { label: '教育訓練', icon: 'i-lucide-graduation-cap', to: '/hrm/training' },
  { label: '招募管理', icon: 'i-lucide-briefcase', to: '/hrm/recruitment' },
]

const crmItems = [
  { label: '總覽', icon: 'i-lucide-layout-dashboard', to: '/crm' },
  {
    label: '客戶管理',
    icon: 'i-lucide-contact',
    defaultOpen: true,
    children: [
      { label: '客戶列表', icon: 'i-lucide-list', to: '/crm/customer' },
      { label: '新增客戶', icon: 'i-lucide-plus', to: '/crm/customer/new' },
    ],
  },
  { label: '商機管理', icon: 'i-lucide-target', to: '/crm/opportunity' },
  { label: '合約管理', icon: 'i-lucide-file-signature', to: '/crm/contract' },
  { label: '行銷活動', icon: 'i-lucide-megaphone', to: '/crm/campaign' },
  { label: '客服工單', icon: 'i-lucide-headset', to: '/crm/ticket' },
  { label: '報表分析', icon: 'i-lucide-chart-bar', to: '/crm/report' },
]

const sidebarItemsMap: Record<string, typeof personalItems> = {
  personal: personalItems,
  foundation: foundationItems,
  erp: erpItems,
  hrm: hrmItems,
  crm: crmItems,
}

const sidebarItems = computed(() => {
  const mod = currentModule.value
  return mod ? (sidebarItemsMap[mod.label.toLowerCase()] ?? personalItems) : personalItems
})
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
