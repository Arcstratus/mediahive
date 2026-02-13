import type { DemoRole } from '~/types'

// TODO: 後端支援 - 改為從 API 取得角色資料
const demoRoles: DemoRole[] = [
  {
    id: 1,
    name: '系統管理員',
    description: '擁有系統所有功能的完整存取權限',
    userCount: 2,
    permissions: ['系統設定', '使用者管理', '角色管理', '部門管理', '稽核日誌', '通知管理'],
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: '部門主管',
    description: '可管理所屬部門的成員與相關資源',
    userCount: 5,
    permissions: ['使用者檢視', '部門管理', '報表檢視'],
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 3,
    name: '一般使用者',
    description: '基本系統使用權限，可存取已授權的模組',
    userCount: 30,
    permissions: ['個人資料', '資源檢視', '書籤管理'],
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 4,
    name: '稽核人員',
    description: '可檢視稽核日誌與系統操作紀錄',
    userCount: 2,
    permissions: ['稽核日誌', '報表檢視', '使用者檢視'],
    created_at: '2024-02-15T00:00:00Z',
  },
]

export function useDemoRoles() {
  const roles = ref<DemoRole[]>(demoRoles)

  function findById(id: number) {
    return roles.value.find(r => r.id === id) ?? null
  }

  return { roles, findById }
}
