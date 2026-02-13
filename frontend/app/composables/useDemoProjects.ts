import type { DemoProject, DemoMilestone, DemoRequirement, ProjectStatus, MilestoneStatus, RequirementStatus, RequirementPriority } from '~/types'

// TODO: 後端支援 - 改為從 API 取得專案資料

const demoProjects: DemoProject[] = [
  {
    id: 1, code: 'PRJ-001', name: 'ERP 系統導入', description: '為客戶導入完整 ERP 系統，包含庫存、採購、銷售及財務模組。',
    customer: '台灣科技股份有限公司', manager: '陳大文', members: ['陳大文', '李國華', '王志明'],
    start_date: '2025-01-01', end_date: '2025-06-30', progress: 35, status: '進行中', budget: 2500000,
    created_at: '2024-12-15T08:00:00Z', updated_at: '2025-03-01T10:00:00Z',
  },
  {
    id: 2, code: 'PRJ-002', name: '官網改版專案', description: '重新設計公司官方網站，提升品牌形象與使用者體驗。',
    customer: '新創數位有限公司', manager: '林小美', members: ['林小美', '張雅婷'],
    start_date: '2025-02-01', end_date: '2025-04-30', progress: 10, status: '規劃中', budget: 800000,
    created_at: '2025-01-20T08:00:00Z', updated_at: '2025-02-01T08:00:00Z',
  },
  {
    id: 3, code: 'PRJ-003', name: '雲端遷移服務', description: '將客戶既有的地端伺服器架構遷移至雲端環境，確保高可用與彈性擴展。',
    customer: '永豐製造股份有限公司', manager: '王志明', members: ['王志明', '李國華', '陳大文'],
    start_date: '2024-10-01', end_date: '2025-03-31', progress: 80, status: '進行中', budget: 1800000,
    created_at: '2024-09-15T08:00:00Z', updated_at: '2025-02-20T08:00:00Z',
  },
  {
    id: 4, code: 'PRJ-004', name: '智慧工廠方案', description: '導入 IoT 與智慧製造方案，實現工廠自動化監控與數據分析。',
    customer: '綠能環保科技公司', manager: '張雅婷', members: ['張雅婷', '王志明'],
    start_date: '2024-08-01', end_date: '2024-12-31', progress: 100, status: '已完成', budget: 3200000,
    created_at: '2024-07-10T08:00:00Z', updated_at: '2024-12-31T08:00:00Z',
  },
  {
    id: 5, code: 'PRJ-005', name: '年度維護合約', description: '提供全年度系統維護與技術支援服務，含 SLA 保障。',
    customer: '大眾貿易有限公司', manager: '李國華', members: ['李國華'],
    start_date: '2025-01-01', end_date: '2025-12-31', progress: 5, status: '進行中', budget: 600000,
    created_at: '2024-12-20T08:00:00Z', updated_at: '2025-01-15T08:00:00Z',
  },
]

const demoMilestones: DemoMilestone[] = [
  { id: 1, projectId: 1, title: '階段一：需求與設計', description: '完成需求分析、系統架構設計與技術方案確認。', status: '已完成', start_date: '2025-01-01', end_date: '2025-02-28', progress: 100, requirementIds: [1, 2], created_at: '2025-01-02T08:00:00Z' },
  { id: 2, projectId: 1, title: '階段二：核心模組開發', description: '開發庫存與採購核心模組。', status: '進行中', start_date: '2025-03-01', end_date: '2025-04-30', progress: 40, requirementIds: [1, 2], created_at: '2025-01-02T08:00:00Z' },
  { id: 3, projectId: 1, title: '階段三：整合與驗收', description: '完成財務模組開發、系統整合與使用者驗收測試。', status: '未開始', start_date: '2025-05-01', end_date: '2025-06-30', progress: 0, requirementIds: [3], created_at: '2025-01-02T08:00:00Z' },
  { id: 4, projectId: 2, title: '設計與開發', description: '完成視覺設計與前端開發。', status: '進行中', start_date: '2025-02-01', end_date: '2025-03-31', progress: 30, requirementIds: [4], created_at: '2025-02-05T08:00:00Z' },
  { id: 5, projectId: 3, title: '基礎架構遷移', description: '完成資料庫與應用程式的雲端遷移作業。', status: '進行中', start_date: '2024-10-01', end_date: '2025-02-28', progress: 75, requirementIds: [5, 6], created_at: '2024-10-02T08:00:00Z' },
]

export const projectStatusColorMap: Record<ProjectStatus, string> = {
  '規劃中': 'neutral',
  '進行中': 'info',
  '已暫停': 'warning',
  '已完成': 'success',
  '已結案': 'success',
  '已取消': 'error',
}

export const milestoneStatusColorMap: Record<MilestoneStatus, string> = {
  '未開始': 'neutral',
  '進行中': 'info',
  '已完成': 'success',
  '已逾期': 'error',
}

export const requirementStatusColorMap: Record<RequirementStatus, string> = {
  '草稿': 'neutral',
  '已確認': 'info',
  '開發中': 'warning',
  '已交付': 'success',
  '已取消': 'error',
}

export const requirementPriorityColorMap: Record<RequirementPriority, string> = {
  '必要': 'error',
  '重要': 'warning',
  '一般': 'info',
  '可選': 'neutral',
}

const demoRequirements: DemoRequirement[] = [
  { id: 1, projectId: 1, requirementNumber: 'REQ-001', title: '庫存即時更新', description: '當進出貨發生時，庫存數量需即時更新，並反映在所有相關報表中。', status: '開發中', priority: '必要', source: '倉管部', acceptanceCriteria: '1. 進貨後 5 秒內庫存數量更新\n2. 出貨後 5 秒內庫存數量更新\n3. 庫存報表即時反映最新數據', created_at: '2025-01-10T08:00:00Z', updated_at: '2025-02-15T08:00:00Z' },
  { id: 2, projectId: 1, requirementNumber: 'REQ-002', title: '採購審核流程', description: '採購單需經過主管審核後方可執行，支援多層簽核。', status: '已確認', priority: '必要', source: '採購部', acceptanceCriteria: '1. 採購金額 10 萬以下：部門主管審核\n2. 採購金額 10-50 萬：處長審核\n3. 採購金額 50 萬以上：總經理審核', created_at: '2025-01-10T08:00:00Z', updated_at: '2025-01-20T08:00:00Z' },
  { id: 3, projectId: 1, requirementNumber: 'REQ-003', title: '財務報表匯出', description: '支援將財務報表匯出為 Excel 與 PDF 格式。', status: '草稿', priority: '重要', source: '財務部', acceptanceCriteria: '1. 支援 Excel (.xlsx) 格式匯出\n2. 支援 PDF 格式匯出\n3. 報表包含公司 Logo 與頁首頁尾', created_at: '2025-01-15T08:00:00Z', updated_at: '2025-01-15T08:00:00Z' },
  { id: 4, projectId: 2, requirementNumber: 'REQ-004', title: '響應式設計', description: '官網須支援桌面、平板及手機等各種螢幕尺寸。', status: '已確認', priority: '必要', source: '行銷部', acceptanceCriteria: '1. 桌面版（1920px）正常顯示\n2. 平板版（768px）自適應佈局\n3. 手機版（375px）單欄佈局', created_at: '2025-02-06T08:00:00Z', updated_at: '2025-02-10T08:00:00Z' },
  { id: 5, projectId: 3, requirementNumber: 'REQ-005', title: '零停機遷移', description: '遷移過程中服務不可中斷，需採用滾動部署策略。', status: '已交付', priority: '必要', source: '營運部', acceptanceCriteria: '1. 遷移期間服務可用率 99.9%\n2. 資料遷移零遺失\n3. 自動回滾機制', created_at: '2024-10-05T08:00:00Z', updated_at: '2025-02-15T08:00:00Z' },
  { id: 6, projectId: 3, requirementNumber: 'REQ-006', title: '自動擴展能力', description: '雲端環境須具備自動水平擴展能力，應對流量高峰。', status: '開發中', priority: '重要', source: '技術長', acceptanceCriteria: '1. CPU 使用率超過 70% 時自動擴展\n2. 流量降低後 10 分鐘自動縮減\n3. 擴展上限為 10 個節點', created_at: '2024-10-05T08:00:00Z', updated_at: '2025-01-20T08:00:00Z' },
]

export function useDemoProjects() {
  const projects = ref<DemoProject[]>(demoProjects)
  const milestones = ref<DemoMilestone[]>(demoMilestones)
  const requirements = ref<DemoRequirement[]>(demoRequirements)

  function findProjectById(id: number) {
    return projects.value.find(p => p.id === id) ?? null
  }

  function getProjectMilestones(projectId: number) {
    return milestones.value.filter(m => m.projectId === projectId)
  }

  function getProjectRequirements(projectId: number) {
    return requirements.value.filter(r => r.projectId === projectId)
  }

  function findRequirementById(id: number) {
    return requirements.value.find(r => r.id === id) ?? null
  }

  function findMilestoneById(id: number) {
    return milestones.value.find(m => m.id === id) ?? null
  }

  function getProjectsByStatus() {
    const statuses: ProjectStatus[] = ['規劃中', '進行中', '已暫停', '已完成', '已結案', '已取消']
    return statuses.map(status => ({
      status,
      projects: projects.value.filter(p => p.status === status),
    }))
  }

  function getMilestonesByStatus(projectId: number) {
    const projectMilestones = getProjectMilestones(projectId)
    const statuses: MilestoneStatus[] = ['未開始', '進行中', '已完成', '已逾期']
    return statuses.map(status => ({
      status,
      milestones: projectMilestones.filter(m => m.status === status),
    }))
  }

  function getMilestoneRequirements(milestoneId: number) {
    const milestone = findMilestoneById(milestoneId)
    if (!milestone) return []
    return requirements.value.filter(r => milestone.requirementIds.includes(r.id))
  }

  function getUpcomingMilestones() {
    return milestones.value
      .filter(m => m.status === '未開始' || m.status === '進行中')
      .sort((a, b) => a.end_date.localeCompare(b.end_date))
  }

  function getRecentProjects(limit: number) {
    return [...projects.value]
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at))
      .slice(0, limit)
  }

  function getProjectCountByStatus() {
    const statuses: ProjectStatus[] = ['規劃中', '進行中', '已完成', '已結案', '已取消']
    const counts = statuses.map(status => ({
      status,
      count: projects.value.filter(p => p.status === status).length,
    }))
    const total = projects.value.length
    return { counts, total }
  }

  return {
    projects,
    milestones,
    requirements,
    findProjectById,
    getProjectMilestones,
    getProjectRequirements,
    findRequirementById,
    findMilestoneById,
    getProjectsByStatus,
    getMilestonesByStatus,
    getMilestoneRequirements,
    getUpcomingMilestones,
    getRecentProjects,
    getProjectCountByStatus,
  }
}
