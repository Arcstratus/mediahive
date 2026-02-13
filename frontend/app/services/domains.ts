import type { ServiceConfig } from './registry'
import {
  userService,
  departmentService,
  roleService,
  settingsService,
  notificationService,
  auditLogService,
  profileService,
  workspaceService,
  inventoryService,
  purchaseService,
  financeService,
  quoteService,
  invoiceService,
  projectService,
  customerService,
  opportunityService,
  contractService,
  campaignService,
  ticketService,
  employeeService,
  attendanceService,
  payrollService,
  performanceService,
  recruitmentService,
  leaveService,
  resourcesService,
  bookmarksService,
  tagsService,
} from './registry'

export interface DomainConfig {
  id: string
  label: string
  icon: string
  services: ServiceConfig[]
}

export const platformDomain: DomainConfig = {
  id: 'platform',
  label: 'Platform',
  icon: 'i-lucide-settings',
  services: [
    userService,
    departmentService,
    roleService,
    settingsService,
    notificationService,
    auditLogService,
    profileService,
    workspaceService,
  ],
}

export const erpDomain: DomainConfig = {
  id: 'erp',
  label: 'ERP',
  icon: 'i-lucide-package',
  services: [
    inventoryService,
    purchaseService,
    financeService,
    quoteService,
    invoiceService,
    projectService,
  ],
}

export const crmDomain: DomainConfig = {
  id: 'crm',
  label: 'CRM',
  icon: 'i-lucide-handshake',
  services: [
    customerService,
    opportunityService,
    contractService,
    campaignService,
    ticketService,
  ],
}

export const hrmDomain: DomainConfig = {
  id: 'hrm',
  label: 'HRM',
  icon: 'i-lucide-users',
  services: [
    employeeService,
    attendanceService,
    payrollService,
    performanceService,
    recruitmentService,
    leaveService,
  ],
}

export const personalDomain: DomainConfig = {
  id: 'personal',
  label: '個人',
  icon: 'i-lucide-library',
  services: [
    resourcesService,
    bookmarksService,
    tagsService,
  ],
}

export const allDomains: DomainConfig[] = [
  platformDomain,
  erpDomain,
  crmDomain,
  hrmDomain,
  personalDomain,
]

/** 服務 ID → 領域的反向對照表 */
export const serviceToDomain: Record<string, DomainConfig> = (() => {
  const map: Record<string, DomainConfig> = {}
  for (const domain of allDomains) {
    for (const service of domain.services) {
      map[service.id] = domain
    }
  }
  return map
})()
