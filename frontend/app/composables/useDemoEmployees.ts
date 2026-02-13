import type { DemoEmployee } from '~/types'

// TODO: 後端支援 - 改為從 API 取得員工資料
const demoEmployees: DemoEmployee[] = [
  { id: 1, name: '陳大文', email: 'dawen.chen@example.com', phone: '0912-345-678', department: '資訊部', position: '系統工程師', status: 'active', hire_date: '2023-03-15', created_at: '2023-03-15T08:00:00Z' },
  { id: 2, name: '林小美', email: 'xiaomei.lin@example.com', phone: '0923-456-789', department: '人資部', position: '人資專員', status: 'active', hire_date: '2023-06-01', created_at: '2023-06-01T08:00:00Z' },
  { id: 3, name: '王志明', email: 'zhiming.wang@example.com', phone: '0934-567-890', department: '業務部', position: '業務經理', status: 'active', hire_date: '2022-01-10', created_at: '2022-01-10T08:00:00Z' },
  { id: 4, name: '張雅婷', email: 'yating.zhang@example.com', phone: '0945-678-901', department: '財務部', position: '會計師', status: 'inactive', hire_date: '2023-09-01', created_at: '2023-09-01T08:00:00Z' },
  { id: 5, name: '李國華', email: 'guohua.li@example.com', phone: '0956-789-012', department: '研發部', position: '資深工程師', status: 'active', hire_date: '2021-07-15', created_at: '2021-07-15T08:00:00Z' },
]

export function useDemoEmployees() {
  const employees = ref<DemoEmployee[]>(demoEmployees)
  function findById(id: number) { return employees.value.find(e => e.id === id) ?? null }
  return { employees, findById }
}
