// ============================================================================
// Core Models
// ============================================================================

export interface Tag {
  id: number
  name: string
  created_at: string
  resource_count?: number
}

export interface Resource {
  id: number
  category: 'image' | 'video'
  filename: string | null
  title: string | null
  folder: string | null
  thumbnail: string | null
  tags: Tag[]
  created_at: string
}

export interface Bookmark {
  id: number
  title: string
  url: string
  description: string | null
  folder: string | null
  tags: Tag[]
  created_at: string
}

export interface TrashItem {
  id: number
  category: string
  filename: string | null
  title: string | null
  folder: string | null
  created_at: string
  deleted_at: string | null
}

export interface DemoDepartment {
  id: number
  name: string
  parentId: number | null
  head: string
  memberCount: number
  created_at: string
}

export interface DemoRole {
  id: number
  name: string
  description: string
  userCount: number
  permissions: string[]
  created_at: string
}

export interface DemoAuditLog {
  id: number
  user: string
  action: string
  target: string
  detail: string
  ip: string
  created_at: string
}

export interface DemoEmployee {
  id: number
  name: string
  email: string
  phone: string
  department: string
  position: string
  status: 'active' | 'inactive'
  hire_date: string
  created_at: string
}

export type CustomerLevel = 'VIP' | '一般' | '潛在'
export type CustomerStatus = 'active' | 'inactive'
export type CustomerIndustry = '資訊科技' | '國際貿易' | '製造業' | '數位媒體' | '環保科技' | '金融業' | '零售業' | '其他'

export interface DemoCustomer {
  id: number
  name: string
  short_name: string
  tax_id: string
  industry: CustomerIndustry
  level: CustomerLevel
  status: CustomerStatus
  address: string
  phone: string
  fax: string
  website: string
  notes: string
  created_at: string
  updated_at: string
}

export interface DemoContact {
  id: number
  customerId: number
  name: string
  title: string
  email: string
  phone: string
  mobile: string
  is_primary: boolean
  notes: string
  created_at: string
}

export interface DemoUser {
  uuid: string
  name: string
  email: string
  phone: string
  department: string
  role: string
  status: 'active' | 'inactive'
  avatar: string
  created_at: string
}

// ============================================================================
// Project Management Types
// ============================================================================

export type ProjectStatus = '規劃中' | '進行中' | '已暫停' | '已完成' | '已結案' | '已取消'
export type MilestoneStatus = '未開始' | '進行中' | '已完成' | '已逾期'
export type RequirementStatus = '草稿' | '已確認' | '開發中' | '已交付' | '已取消'
export type RequirementPriority = '必要' | '重要' | '一般' | '可選'

export interface DemoProject {
  id: number
  code: string
  name: string
  description: string
  customer: string
  manager: string
  members: string[]
  start_date: string
  end_date: string
  progress: number
  status: ProjectStatus
  budget: number
  created_at: string
  updated_at: string
}

export interface DemoMilestone {
  id: number
  projectId: number
  title: string
  description: string
  status: MilestoneStatus
  start_date: string
  end_date: string
  progress: number
  requirementIds: number[]
  created_at: string
}

export interface DemoRequirement {
  id: number
  projectId: number
  requirementNumber: string
  title: string
  description: string
  status: RequirementStatus
  priority: RequirementPriority
  source: string
  acceptanceCriteria: string
  created_at: string
  updated_at: string
}

// ============================================================================
// API Query Params
// ============================================================================

export interface ResourceListParams {
  page?: number
  per_page?: number
  category?: string
  search?: string
  ext?: string[]
  tag?: string[]
  folder?: string
  sort_by?: string
  sort_desc?: boolean
}

export interface ResourceIdParams {
  category?: string
  search?: string
  ext?: string[]
  tag?: string[]
  folder?: string
  sort_by?: string
  sort_desc?: boolean
}

export interface BookmarkListParams {
  page?: number
  per_page?: number
  search?: string
  tag?: string[]
  folder?: string
  sort_by?: string
  sort_desc?: boolean
}

// ============================================================================
// API Response Types
// ============================================================================

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
}

export interface Stats {
  images: number
  videos: number
  bookmarks: number
  tags: number
}

export interface FolderInfo {
  folder: string
  count: number
}

export interface ScannedFile {
  path: string
  name: string
  type: 'image' | 'video'
  size: number
}

export interface ImportResult {
  imported: number
  skipped: number
}

// ============================================================================
// UI Types
// ============================================================================

export interface FolderNode<T = Resource> {
  children: Map<string, FolderNode<T>>
  items: T[]
}

export interface BreadcrumbItem {
  label: string
  icon?: string
  to?: string
}
