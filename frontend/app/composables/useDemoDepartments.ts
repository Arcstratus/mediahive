import type { DemoDepartment } from '~/types'

// TODO: 後端支援 - 改為從 API 取得部門資料
const demoDepartments: DemoDepartment[] = [
  { id: 1, name: '總經理室', parentId: null, head: '李總經理', memberCount: 3, created_at: '2024-01-01T00:00:00Z' },
  { id: 2, name: '資訊部', parentId: 1, head: '陳大文', memberCount: 8, created_at: '2024-01-01T00:00:00Z' },
  { id: 3, name: '人資部', parentId: 1, head: '林小美', memberCount: 5, created_at: '2024-01-01T00:00:00Z' },
  { id: 4, name: '財務部', parentId: 1, head: '張雅婷', memberCount: 6, created_at: '2024-01-01T00:00:00Z' },
  { id: 5, name: '業務部', parentId: 1, head: '王志明', memberCount: 12, created_at: '2024-01-01T00:00:00Z' },
  { id: 6, name: '研發部', parentId: 1, head: '李國華', memberCount: 15, created_at: '2024-01-01T00:00:00Z' },
  { id: 7, name: '國內業務組', parentId: 5, head: '黃小華', memberCount: 6, created_at: '2024-03-01T00:00:00Z' },
  { id: 8, name: '海外業務組', parentId: 5, head: '劉明哲', memberCount: 6, created_at: '2024-03-01T00:00:00Z' },
  { id: 9, name: '前端組', parentId: 6, head: '周小龍', memberCount: 7, created_at: '2024-03-01T00:00:00Z' },
  { id: 10, name: '後端組', parentId: 6, head: '吳大偉', memberCount: 8, created_at: '2024-03-01T00:00:00Z' },
]

export interface DepartmentTreeNode {
  department: DemoDepartment
  children: DepartmentTreeNode[]
}

export function useDemoDepartments() {
  const departments = ref<DemoDepartment[]>(demoDepartments)

  function findById(id: number) {
    return departments.value.find(d => d.id === id) ?? null
  }

  const tree = computed<DepartmentTreeNode[]>(() => {
    const map = new Map<number, DepartmentTreeNode>()
    const roots: DepartmentTreeNode[] = []

    for (const dept of departments.value) {
      map.set(dept.id, { department: dept, children: [] })
    }

    for (const dept of departments.value) {
      const node = map.get(dept.id)!
      if (dept.parentId === null) {
        roots.push(node)
      }
      else {
        const parent = map.get(dept.parentId)
        if (parent) parent.children.push(node)
      }
    }

    return roots
  })

  return { departments, findById, tree }
}
