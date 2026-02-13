# Mediahive 專案結構規格書

> 本文件用於討論與確立系統架構、服務劃分、前端組織結構
> 商業模式：賣「服務」給不同產業的小型公司，客戶按需組合

---

## 核心架構概念

### 領域 vs 服務

| 概念 | 性質 | 說明 | 舉例 |
|---|---|---|---|
| **領域 (Domain)** | 虛的 | 一組服務的商業分類，用於導航和銷售包裝 | ERP、HRM、CRM |
| **服務 (Service)** | 實的 | 獨立可交付的功能單元，客戶購買的最小粒度 | 專案管理、考勤管理、客戶管理 |
| **平台 (Platform)** | 基礎 | 所有服務共用的底層能力 | 使用者管理、權限、BPM 簽核 |

### 設計原則

1. **服務是一等公民** — 路由、頁面、元件、composable 以服務為單位組織
2. **領域是配置** — 領域只決定「哪些服務放在一起展示」，不影響路由和檔案結構
3. **服務可獨立交付** — 每個服務可以單獨賣給客戶，不依賴同領域的其他服務
4. **服務可跨領域** — 同一個服務可以出現在不同的領域組合中
5. **服務可自訂 layout** — 大部分用 dashboard layout，但 CMS 等特殊服務可以用自己的 layout
6. **底層資料共用** — 服務之間的關聯透過共用資料（如：專案服務讀取人員資料），不是服務合併

---

## 決議紀錄

以下為已確認的架構決策：

### 路由結構
- **採用扁平路由**：以服務為前綴（`/project`、`/customer`），不以領域為前綴（~~`/erp/project`~~）

### 領域頁面
- **現階段不做**：領域是套裝概念，未來可作為服務提供不同職位的 summary，但當前省略

### 首頁 `/`
- **簡易導航頁**：列出所有可用的服務/領域入口，方便開發時快速跳轉
- 不做儀表板（因職權不同，複雜度高）

### 工時管理
- **不做**：移除此服務

### 個人 (Personal)
- **命名為「個人」**：不使用 PRM 縮寫
- **資源共享**：未來「空間 (Workspace)」會獨立成服務，處理跨人/跨部門的共享資源
  - 人是被授權者或檔案擁有者
  - 空間是服務，負責共享機制
  - 現階段不實作，路由設計上預留

### 合約管理歸屬
- **待決定**：歸類只影響領域 sidebar 分組，不影響路由。之後配置領域時再決定

### 遷移策略
- **一次性遷移**：舊頁面搬到對應新路徑
- **Demo 頁面全部保留並遷移**，新路徑也要有對應 demo 頁面

---

## 服務清單

### 平台服務（Platform）

每個部署都包含，不單獨銷售。

| 服務 ID | 名稱 | 說明 | 路由前綴 |
|---|---|---|---|
| `user` | 使用者管理 | 帳號 CRUD、個人資料 | `/user` |
| `department` | 部門管理 | 組織架構、樹狀圖 | `/department` |
| `role` | 角色權限 | 角色 CRUD、權限分配 | `/role` |
| `settings` | 系統設定 | 全域參數、郵件、安全性 | `/settings` |
| `notification` | 通知管理 | 通知範本、推播設定 | `/notification` |
| `audit-log` | 稽核日誌 | 操作紀錄（唯讀） | `/audit-log` |
| `profile` | 個人資料 | 登入者自己的資料編輯 | `/profile` |
| `bpm` | 簽核流程 | 跨服務的審核機制（待設計） | `/bpm` |

### 業務服務（Business）

按需銷售，可自由組合。

| 服務 ID | 名稱 | 常見歸屬領域 | 說明 | 路由前綴 | Layout |
|---|---|---|---|---|---|
| `project` | 專案管理 | ERP | 專案 CRUD、看板、里程碑 | `/project` | dashboard |
| `quote` | 報價管理 | ERP | 報價單 CRUD | `/quote` | dashboard |
| `invoice` | 請款管理 | ERP | 請款單 CRUD、收款追蹤 | `/invoice` | dashboard |
| `finance` | 財務報表 | ERP | 收支摘要、報表 | `/finance` | dashboard |
| `inventory` | 庫存管理 | ERP | 品項、庫存數量 | `/inventory` | dashboard |
| `purchase` | 採購管理 | ERP | 採購單、供應商 | `/purchase` | dashboard |
| `customer` | 客戶管理 | CRM | 客戶 CRUD、聯絡紀錄 | `/customer` | dashboard |
| `opportunity` | 商機管理 | CRM | 銷售漏斗、階段追蹤 | `/opportunity` | dashboard |
| `contract` | 合約管理 | CRM/ERP（待定） | 合約簽訂、到期管理 | `/contract` | dashboard |
| `campaign` | 行銷活動 | CRM | 活動管理、成效追蹤 | `/campaign` | dashboard |
| `ticket` | 客服工單 | CRM | 工單 CRUD、SLA | `/ticket` | dashboard |
| `employee` | 員工管理 | HRM | 員工 CRUD、到離職 | `/employee` | dashboard |
| `attendance` | 出勤管理 | HRM | 打卡、出勤紀錄 | `/attendance` | dashboard |
| `leave` | 請假管理 | HRM | 假單申請、審核 | `/leave` | dashboard |
| `payroll` | 薪資管理 | HRM | 薪資計算、發放 | `/payroll` | dashboard |
| `performance` | 績效考核 | HRM | KPI、評核 | `/performance` | dashboard |
| `recruitment` | 招募管理 | HRM | 職缺、面試 | `/recruitment` | dashboard |
| `resource` | 資源管理 | 個人 | 多媒體資源 | `/resources` | dashboard |
| `bookmark` | 書籤管理 | 個人 | 網路書籤 | `/bookmarks` | dashboard |
| `tag` | 標籤管理 | 個人 | 分類標籤 | `/tags` | dashboard |
| `workspace` | 共享空間 | （獨立） | 跨人/跨部門資源共享（未來） | `/workspace` | dashboard |
| `cms` | 內容管理 | — | 頁面編輯、發布 | `/cms` | **cms** (自訂) |

---

## 領域配置

領域是服務的分組，純粹用於：
1. Navbar 下拉選單的選項
2. Sidebar 顯示哪些服務
3. 銷售時的包裝口徑

```ts
// 概念示意，非最終程式碼
const domains = {
  platform: {
    label: 'Platform',
    icon: 'i-lucide-settings',
    services: ['user', 'department', 'role', 'settings', 'notification', 'audit-log', 'profile', 'bpm'],
  },
  erp: {
    label: 'ERP',
    icon: 'i-lucide-package',
    services: ['project', 'quote', 'invoice', 'finance', 'inventory', 'purchase'],
  },
  crm: {
    label: 'CRM',
    icon: 'i-lucide-handshake',
    services: ['customer', 'opportunity', 'contract', 'campaign', 'ticket'],
  },
  hrm: {
    label: 'HRM',
    icon: 'i-lucide-users',
    services: ['employee', 'attendance', 'leave', 'payroll', 'performance', 'recruitment'],
  },
  personal: {
    label: '個人',
    icon: 'i-lucide-library',
    services: ['resource', 'bookmark', 'tag'],
  },
}
```

### 客戶 A（接案公司）購買的組合

```
Platform（必含）+ project + customer + contract + employee + attendance + leave
```

### 客戶 B（電商）購買的組合

```
Platform（必含）+ inventory + purchase + customer + ticket + cms
```

領域分組可以按客戶需求重新排列，不影響服務本身。

---

## 前端目錄結構

### 現況

```
frontend/app/
  pages/
    foundation/        ← 領域為目錄
      user/
      department/
      ...
    erp/
      inventory.vue
      ...
    crm/
      customer/
      ...
```

路由綁定在領域上 (`/foundation/user`, `/erp/inventory`)，服務無法獨立抽離。

### 目標：服務為核心

```
frontend/app/
  services/                          ← 服務定義（metadata + sidebar config）
    registry.ts                      ← 服務註冊表
    domains.ts                       ← 領域分組配置

  pages/                             ← 路由以服務為前綴，不以領域
    index.vue                        ← 導航頁：列出所有服務/領域入口
    user/                            ← Platform: 使用者管理
      index.vue
      new.vue
      [uuid].vue
    department/                      ← Platform: 部門管理
      index.vue
      new.vue
      [id].vue
    role/                            ← Platform: 角色權限
      index.vue
      new.vue
      [id].vue
    settings.vue                     ← Platform: 系統設定
    notification.vue                 ← Platform: 通知管理
    audit-log.vue                    ← Platform: 稽核日誌
    profile.vue                      ← Platform: 個人資料
    project/                         ← ERP: 專案管理
      index.vue
      new.vue
      [id]/
        index.vue
        edit.vue
    quote/                           ← ERP: 報價管理
      index.vue
      new.vue
      [id].vue
    invoice/                         ← ERP: 請款管理
      index.vue
      new.vue
      [id].vue
    finance.vue                      ← ERP: 財務報表
    inventory.vue                    ← ERP: 庫存管理
    purchase.vue                     ← ERP: 採購管理
    customer/                        ← CRM: 客戶管理
      index.vue
      new.vue
      [id].vue
    opportunity.vue                  ← CRM: 商機管理
    contract.vue                     ← CRM: 合約管理
    campaign.vue                     ← CRM: 行銷活動
    ticket.vue                       ← CRM: 客服工單
    employee/                        ← HRM: 員工管理
      index.vue
      new.vue
      [id].vue
    attendance.vue                   ← HRM: 出勤管理
    leave.vue                        ← HRM: 請假管理
    payroll.vue                      ← HRM: 薪資管理
    performance.vue                  ← HRM: 績效考核
    recruitment.vue                  ← HRM: 招募管理
    resources/                       ← 個人: 資源管理（已存在）
    bookmarks/                       ← 個人: 書籤管理（已存在）
    tags/                            ← 個人: 標籤管理（已存在）

  layouts/
    dashboard.vue                    ← 通用 layout（大部分服務）
    cms.vue                          ← CMS 專用 layout（未來）
    auth.vue                         ← 登入 layout（未來）

  components/
    Nav*.vue                         ← Navbar 相關元件
    PageBreadcrumb.vue
    DepartmentTreeItem.vue
    UserFormLayout.vue
    ...                              ← 共用 UI 元件

  composables/
    useServiceRegistry.ts            ← 讀取服務/領域配置
    useApiFetch.ts
    ...
```

### 路由對照（現況 → 目標）

| 現況 | 目標 | 說明 |
|---|---|---|
| `/foundation/user` | `/user` | 平台服務，不需要領域前綴 |
| `/foundation/department` | `/department` | 同上 |
| `/foundation/role` | `/role` | 同上 |
| `/foundation/settings` | `/settings` | 同上 |
| `/foundation/notification` | `/notification` | 同上 |
| `/foundation/audit-log` | `/audit-log` | 同上 |
| `/foundation/profile` | `/profile` | 同上 |
| `/erp` | （移除） | 領域不再有頁面 |
| `/erp/inventory` | `/inventory` | 服務獨立路由 |
| `/erp/purchase` | `/purchase` | 同上 |
| `/erp/sales` | （移除） | 拆分為 quote + invoice |
| `/erp/finance` | `/finance` | 服務獨立路由 |
| `/erp/production` | （移除） | 不在服務清單中 |
| `/erp/logistics` | （移除） | 不在服務清單中 |
| `/crm` | （移除） | 領域不再有頁面 |
| `/crm/customer` | `/customer` | 服務獨立路由 |
| `/crm/opportunity` | `/opportunity` | 同上 |
| `/crm/contract` | `/contract` | 同上 |
| `/crm/campaign` | `/campaign` | 同上 |
| `/crm/ticket` | `/ticket` | 同上 |
| `/crm/report` | （移除） | 各服務內建報表 |
| `/hrm` | （移除） | 領域不再有頁面 |
| `/hrm/employee` | `/employee` | 服務獨立路由 |
| `/hrm/attendance` | `/attendance` | 同上 |
| `/hrm/payroll` | `/payroll` | 同上 |
| `/hrm/performance` | `/performance` | 同上 |
| `/hrm/training` | （移除） | 不在服務清單中 |
| `/hrm/recruitment` | `/recruitment` | 同上 |
| `/personal` | （移除） | 領域不再有頁面 |
| `/resources` | `/resources` | 不變 |
| `/bookmarks` | `/bookmarks` | 不變 |
| `/tags` | `/tags` | 不變 |
| `/foundation` | （移除） | 領域不再有頁面 |
| （新增） | `/leave` | 新服務：請假管理 |
| （新增） | `/project` | 新服務：專案管理 |
| （新增） | `/quote` | 新服務：報價管理 |
| （新增） | `/invoice` | 新服務：請款管理 |

---

## 服務註冊表（概念設計）

```ts
// services/registry.ts
export interface ServiceConfig {
  id: string
  label: string
  icon: string
  path: string                       // 路由前綴
  layout?: string                    // 預設 'dashboard'
  sidebar: SidebarItem[]             // 該服務在 sidebar 中的項目
}

export const services: Record<string, ServiceConfig> = {
  user: {
    id: 'user',
    label: '使用者管理',
    icon: 'i-lucide-users',
    path: '/user',
    sidebar: [
      { label: '使用者列表', icon: 'i-lucide-list', to: '/user' },
      { label: '新增使用者', icon: 'i-lucide-plus', to: '/user/new' },
    ],
  },
  project: {
    id: 'project',
    label: '專案管理',
    icon: 'i-lucide-folder-kanban',
    path: '/project',
    sidebar: [
      { label: '專案列表', icon: 'i-lucide-list', to: '/project' },
      { label: '新建專案', icon: 'i-lucide-plus', to: '/project/new' },
    ],
  },
  // ... 其餘服務
}
```

---

## Dashboard Layout 運作方式

```
1. 使用者進入某個路由，例如 /project/123
2. dashboard.vue 用 route.path 比對 services registry，找到 service = 'project'
3. 從 domains config 找到 project 屬於 'erp' 領域
4. Navbar 下拉選單高亮 'ERP'
5. Sidebar 顯示 erp 領域下所有服務的 sidebar items
6. 切換領域 → navigateTo 到該領域第一個服務的首頁
```

---

## BPM 簽核流程（概要）

跨服務的審核機制，例如：
- 請假申請 → 主管簽核
- 報價單 → 主管簽核 → 客戶確認
- 採購單 → 主管簽核 → 財務簽核

### 設計方向
- BPM 是平台服務，提供通用的簽核引擎
- 各業務服務透過 API 發起簽核流程
- BPM 服務有自己的管理頁面：流程定義、簽核紀錄
- 高度客製化：每個客戶的簽核規則不同，先建骨架即可

### 頁面（未來）
| 路由 | 頁面 |
|---|---|
| `/bpm` | 我的待簽核 |
| `/bpm/history` | 簽核紀錄 |
| `/bpm/flow` | 流程定義（管理員） |
