import type { DemoAuditLog } from '~/types'

// TODO: 後端支援 - 改為從 API 取得稽核日誌
const demoAuditLogs: DemoAuditLog[] = [
  { id: 1, user: '陳大文', action: '登入', target: '系統', detail: '使用者登入系統', ip: '192.168.1.100', created_at: '2025-06-01T09:00:00Z' },
  { id: 2, user: '陳大文', action: '新增', target: '使用者', detail: '新增使用者「林小美」', ip: '192.168.1.100', created_at: '2025-06-01T09:15:00Z' },
  { id: 3, user: '林小美', action: '登入', target: '系統', detail: '使用者登入系統', ip: '192.168.1.101', created_at: '2025-06-01T10:00:00Z' },
  { id: 4, user: '陳大文', action: '修改', target: '系統設定', detail: '變更郵件伺服器設定', ip: '192.168.1.100', created_at: '2025-06-01T11:30:00Z' },
  { id: 5, user: '王志明', action: '刪除', target: '資源', detail: '刪除資源「產品型錄.pdf」', ip: '192.168.1.102', created_at: '2025-06-01T14:00:00Z' },
  { id: 6, user: '李國華', action: '修改', target: '部門', detail: '更新研發部門資訊', ip: '192.168.1.103', created_at: '2025-06-02T08:30:00Z' },
  { id: 7, user: '張雅婷', action: '匯出', target: '報表', detail: '匯出月度財務報表', ip: '192.168.1.104', created_at: '2025-06-02T10:00:00Z' },
  { id: 8, user: '陳大文', action: '修改', target: '角色', detail: '更新「部門主管」角色權限', ip: '192.168.1.100', created_at: '2025-06-02T15:00:00Z' },
]

export function useDemoAuditLogs() {
  const logs = ref<DemoAuditLog[]>(demoAuditLogs)
  return { logs }
}
