import type { DemoUser } from '~/types'

// TODO: 後端支援 - 改為從 API 取得使用者資料
const demoUsers: DemoUser[] = [
  {
    uuid: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    name: '陳大文',
    email: 'dawen.chen@example.com',
    phone: '0912-345-678',
    department: '資訊部',
    role: '系統管理員',
    status: 'active',
    avatar: '',
    created_at: '2025-01-15T08:30:00Z',
  },
  {
    uuid: 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    name: '林小美',
    email: 'xiaomei.lin@example.com',
    phone: '0923-456-789',
    department: '人資部',
    role: '部門主管',
    status: 'active',
    avatar: '',
    created_at: '2025-02-20T10:15:00Z',
  },
  {
    uuid: 'c3d4e5f6-a7b8-9012-cdef-123456789012',
    name: '王志明',
    email: 'zhiming.wang@example.com',
    phone: '0934-567-890',
    department: '業務部',
    role: '一般使用者',
    status: 'active',
    avatar: '',
    created_at: '2025-03-10T14:00:00Z',
  },
  {
    uuid: 'd4e5f6a7-b8c9-0123-defa-234567890123',
    name: '張雅婷',
    email: 'yating.zhang@example.com',
    phone: '0945-678-901',
    department: '財務部',
    role: '一般使用者',
    status: 'inactive',
    avatar: '',
    created_at: '2025-04-05T09:45:00Z',
  },
  {
    uuid: 'e5f6a7b8-c9d0-1234-efab-345678901234',
    name: '李國華',
    email: 'guohua.li@example.com',
    phone: '0956-789-012',
    department: '研發部',
    role: '部門主管',
    status: 'active',
    avatar: '',
    created_at: '2025-05-12T11:30:00Z',
  },
]

export function useDemoUsers() {
  const users = ref<DemoUser[]>(demoUsers)

  function findByUuid(uuid: string) {
    return users.value.find(u => u.uuid === uuid) ?? null
  }

  return { users, findByUuid }
}
