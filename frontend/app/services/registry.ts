export interface SidebarItem {
  label: string
  icon: string
  to?: string
  defaultOpen?: boolean
  children?: SidebarItem[]
}

export interface ServiceConfig {
  id: string
  label: string
  icon: string
  path: string
  sidebar: SidebarItem[]
}

// ── Platform 服務 ──

export const userService: ServiceConfig = {
  id: 'user',
  label: '使用者管理',
  icon: 'i-lucide-users',
  path: '/user',
  sidebar: [
    { label: '使用者列表', icon: 'i-lucide-list', to: '/user' },
    { label: '新增使用者', icon: 'i-lucide-plus', to: '/user/new' },
  ],
}

export const departmentService: ServiceConfig = {
  id: 'department',
  label: '組織架構',
  icon: 'i-lucide-building',
  path: '/department',
  sidebar: [
    { label: '部門列表', icon: 'i-lucide-list', to: '/department' },
    { label: '新增部門', icon: 'i-lucide-plus', to: '/department/new' },
  ],
}

export const roleService: ServiceConfig = {
  id: 'role',
  label: '角色權限',
  icon: 'i-lucide-shield',
  path: '/role',
  sidebar: [
    { label: '角色列表', icon: 'i-lucide-list', to: '/role' },
    { label: '新增角色', icon: 'i-lucide-plus', to: '/role/new' },
  ],
}

export const settingsService: ServiceConfig = {
  id: 'settings',
  label: '系統設定',
  icon: 'i-lucide-settings',
  path: '/settings',
  sidebar: [],
}

export const notificationService: ServiceConfig = {
  id: 'notification',
  label: '通知中心',
  icon: 'i-lucide-bell',
  path: '/notification',
  sidebar: [],
}

export const auditLogService: ServiceConfig = {
  id: 'audit-log',
  label: '稽核日誌',
  icon: 'i-lucide-scroll-text',
  path: '/audit-log',
  sidebar: [],
}

export const profileService: ServiceConfig = {
  id: 'profile',
  label: '個人資料',
  icon: 'i-lucide-user',
  path: '/profile',
  sidebar: [],
}

export const workspaceService: ServiceConfig = {
  id: 'workspace',
  label: '工作區',
  icon: 'i-lucide-layout-dashboard',
  path: '/workspace',
  sidebar: [],
}

// ── ERP 服務 ──

export const inventoryService: ServiceConfig = {
  id: 'inventory',
  label: '庫存管理',
  icon: 'i-lucide-warehouse',
  path: '/inventory',
  sidebar: [],
}

export const purchaseService: ServiceConfig = {
  id: 'purchase',
  label: '採購管理',
  icon: 'i-lucide-shopping-cart',
  path: '/purchase',
  sidebar: [],
}

export const financeService: ServiceConfig = {
  id: 'finance',
  label: '財務會計',
  icon: 'i-lucide-calculator',
  path: '/finance',
  sidebar: [],
}

export const quoteService: ServiceConfig = {
  id: 'quote',
  label: '報價管理',
  icon: 'i-lucide-file-text',
  path: '/quote',
  sidebar: [
    { label: '報價列表', icon: 'i-lucide-list', to: '/quote' },
    { label: '新增報價', icon: 'i-lucide-plus', to: '/quote/new' },
  ],
}

export const invoiceService: ServiceConfig = {
  id: 'invoice',
  label: '請款管理',
  icon: 'i-lucide-receipt',
  path: '/invoice',
  sidebar: [
    { label: '請款列表', icon: 'i-lucide-list', to: '/invoice' },
    { label: '新增請款', icon: 'i-lucide-plus', to: '/invoice/new' },
  ],
}

export const projectService: ServiceConfig = {
  id: 'project',
  label: '專案管理',
  icon: 'i-lucide-folder-kanban',
  path: '/project',
  sidebar: [
    { label: '專案總覽', icon: 'i-lucide-layout-dashboard', to: '/project/dashboard' },
    { label: '專案列表', icon: 'i-lucide-list', to: '/project' },
    { label: '新增專案', icon: 'i-lucide-plus', to: '/project/new' },
  ],
}

// ── CRM 服務 ──

export const customerService: ServiceConfig = {
  id: 'customer',
  label: '客戶管理',
  icon: 'i-lucide-contact',
  path: '/customer',
  sidebar: [
    { label: '客戶總覽', icon: 'i-lucide-layout-dashboard', to: '/customer/dashboard' },
    { label: '客戶列表', icon: 'i-lucide-list', to: '/customer' },
    { label: '新增客戶', icon: 'i-lucide-plus', to: '/customer/new' },
  ],
}

export const opportunityService: ServiceConfig = {
  id: 'opportunity',
  label: '商機管理',
  icon: 'i-lucide-target',
  path: '/opportunity',
  sidebar: [],
}

export const contractService: ServiceConfig = {
  id: 'contract',
  label: '合約管理',
  icon: 'i-lucide-file-signature',
  path: '/contract',
  sidebar: [],
}

export const campaignService: ServiceConfig = {
  id: 'campaign',
  label: '行銷活動',
  icon: 'i-lucide-megaphone',
  path: '/campaign',
  sidebar: [],
}

export const ticketService: ServiceConfig = {
  id: 'ticket',
  label: '客服工單',
  icon: 'i-lucide-headset',
  path: '/ticket',
  sidebar: [],
}

// ── HRM 服務 ──

export const employeeService: ServiceConfig = {
  id: 'employee',
  label: '員工管理',
  icon: 'i-lucide-user',
  path: '/employee',
  sidebar: [
    { label: '員工列表', icon: 'i-lucide-list', to: '/employee' },
    { label: '新增員工', icon: 'i-lucide-plus', to: '/employee/new' },
  ],
}

export const attendanceService: ServiceConfig = {
  id: 'attendance',
  label: '出勤管理',
  icon: 'i-lucide-clock',
  path: '/attendance',
  sidebar: [],
}

export const payrollService: ServiceConfig = {
  id: 'payroll',
  label: '薪資管理',
  icon: 'i-lucide-banknote',
  path: '/payroll',
  sidebar: [],
}

export const performanceService: ServiceConfig = {
  id: 'performance',
  label: '績效考核',
  icon: 'i-lucide-trophy',
  path: '/performance',
  sidebar: [],
}

export const recruitmentService: ServiceConfig = {
  id: 'recruitment',
  label: '招募管理',
  icon: 'i-lucide-briefcase',
  path: '/recruitment',
  sidebar: [],
}

export const leaveService: ServiceConfig = {
  id: 'leave',
  label: '請假管理',
  icon: 'i-lucide-calendar-off',
  path: '/leave',
  sidebar: [],
}

// ── 個人服務 ──

export const resourcesService: ServiceConfig = {
  id: 'resources',
  label: '資源管理',
  icon: 'i-lucide-library',
  path: '/resources',
  sidebar: [
    { label: '資源列表', icon: 'i-lucide-list', to: '/resources' },
    { label: '資料夾', icon: 'i-lucide-folders', to: '/resources/folders' },
    { label: '回收桶', icon: 'i-lucide-trash-2', to: '/resources/trash' },
  ],
}

export const bookmarksService: ServiceConfig = {
  id: 'bookmarks',
  label: '書籤管理',
  icon: 'i-lucide-bookmark',
  path: '/bookmarks',
  sidebar: [
    { label: '書籤列表', icon: 'i-lucide-list', to: '/bookmarks' },
    { label: '資料夾', icon: 'i-lucide-folders', to: '/bookmarks/folders' },
  ],
}

export const tagsService: ServiceConfig = {
  id: 'tags',
  label: '標籤管理',
  icon: 'i-lucide-tag',
  path: '/tags',
  sidebar: [
    { label: '標籤列表', icon: 'i-lucide-list', to: '/tags' },
  ],
}

// ── 全部服務列表 ──

export const allServices: ServiceConfig[] = [
  // Platform
  userService,
  departmentService,
  roleService,
  settingsService,
  notificationService,
  auditLogService,
  profileService,
  workspaceService,
  // ERP
  inventoryService,
  purchaseService,
  financeService,
  quoteService,
  invoiceService,
  projectService,
  // CRM
  customerService,
  opportunityService,
  contractService,
  campaignService,
  ticketService,
  // HRM
  employeeService,
  attendanceService,
  payrollService,
  performanceService,
  recruitmentService,
  leaveService,
  // 個人
  resourcesService,
  bookmarksService,
  tagsService,
]
