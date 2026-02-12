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
