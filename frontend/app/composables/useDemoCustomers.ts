import type { DemoCustomer, DemoContact, CustomerLevel, CustomerStatus, CustomerIndustry } from '~/types'

// TODO: 後端支援 - 改為從 API 取得客戶資料

export const customerLevelColorMap: Record<CustomerLevel, string> = {
  'VIP': 'warning',
  '一般': 'info',
  '潛在': 'neutral',
}

export const customerStatusColorMap: Record<CustomerStatus, string> = {
  'active': 'success',
  'inactive': 'neutral',
}

const demoCustomers: DemoCustomer[] = [
  {
    id: 1, name: '台灣科技股份有限公司', short_name: '台科', tax_id: '12345678',
    industry: '資訊科技', level: 'VIP', status: 'active',
    address: '台北市信義區信義路五段 7 號', phone: '02-1234-5678', fax: '02-1234-5679',
    website: 'https://twtech.com.tw', notes: '長期合作夥伴，ERP 系統導入中。',
    created_at: '2024-01-15T08:00:00Z', updated_at: '2025-03-01T10:00:00Z',
  },
  {
    id: 2, name: '大眾貿易有限公司', short_name: '大眾', tax_id: '23456789',
    industry: '國際貿易', level: '一般', status: 'active',
    address: '台北市中山區南京東路三段 168 號', phone: '02-2345-6789', fax: '02-2345-6780',
    website: 'https://dazhong.com.tw', notes: '年度維護合約客戶。',
    created_at: '2024-03-20T10:00:00Z', updated_at: '2025-01-15T08:00:00Z',
  },
  {
    id: 3, name: '永豐製造股份有限公司', short_name: '永豐', tax_id: '34567890',
    industry: '製造業', level: '一般', status: 'active',
    address: '台中市西屯區工業區一路 100 號', phone: '04-3456-7890', fax: '04-3456-7891',
    website: 'https://yongfeng.com.tw', notes: '雲端遷移服務進行中。',
    created_at: '2024-05-10T14:00:00Z', updated_at: '2025-02-20T08:00:00Z',
  },
  {
    id: 4, name: '新創數位有限公司', short_name: '新創', tax_id: '45678901',
    industry: '數位媒體', level: '潛在', status: 'active',
    address: '台北市松山區敦化北路 88 號', phone: '02-4567-8901', fax: '',
    website: 'https://newdigital.tw', notes: '官網改版專案洽談中。',
    created_at: '2024-07-01T09:00:00Z', updated_at: '2025-02-01T08:00:00Z',
  },
  {
    id: 5, name: '綠能環保科技公司', short_name: '綠能', tax_id: '56789012',
    industry: '環保科技', level: '潛在', status: 'inactive',
    address: '新竹市東區光復路二段 321 號', phone: '03-5678-9012', fax: '03-5678-9013',
    website: 'https://greentech.com.tw', notes: '智慧工廠方案已完成。',
    created_at: '2024-08-15T11:00:00Z', updated_at: '2024-12-31T08:00:00Z',
  },
  {
    id: 6, name: '鼎新金融控股公司', short_name: '鼎新金控', tax_id: '67890123',
    industry: '金融業', level: 'VIP', status: 'active',
    address: '台北市中正區重慶南路一段 2 號', phone: '02-6789-0123', fax: '02-6789-0124',
    website: 'https://dingxin.com.tw', notes: '核心系統維護合約，高度機敏客戶。',
    created_at: '2024-02-10T08:00:00Z', updated_at: '2025-02-28T08:00:00Z',
  },
  {
    id: 7, name: '百貨通零售集團', short_name: '百貨通', tax_id: '78901234',
    industry: '零售業', level: '一般', status: 'active',
    address: '高雄市前鎮區中山二路 260 號', phone: '07-7890-1234', fax: '07-7890-1235',
    website: 'https://bhmart.com.tw', notes: 'POS 系統整合需求。',
    created_at: '2024-09-05T08:00:00Z', updated_at: '2025-01-20T08:00:00Z',
  },
  {
    id: 8, name: '宏宇國際貿易有限公司', short_name: '宏宇', tax_id: '89012345',
    industry: '國際貿易', level: 'VIP', status: 'active',
    address: '台北市大安區忠孝東路四段 250 號', phone: '02-8901-2345', fax: '02-8901-2346',
    website: 'https://hongyu.com.tw', notes: '跨國物流系統建置案。',
    created_at: '2024-04-18T08:00:00Z', updated_at: '2025-03-10T08:00:00Z',
  },
  {
    id: 9, name: '智慧製造科技公司', short_name: '智造', tax_id: '90123456',
    industry: '製造業', level: '一般', status: 'active',
    address: '桃園市龜山區文化一路 50 號', phone: '03-9012-3456', fax: '03-9012-3457',
    website: '', notes: '',
    created_at: '2025-01-10T08:00:00Z', updated_at: '2025-02-15T08:00:00Z',
  },
  {
    id: 10, name: '快拍影視製作公司', short_name: '快拍', tax_id: '01234567',
    industry: '數位媒體', level: '潛在', status: 'active',
    address: '台北市內湖區瑞光路 513 號', phone: '02-0123-4567', fax: '',
    website: 'https://quickshot.tw', notes: '內容管理平台需求評估中。',
    created_at: '2025-02-01T08:00:00Z', updated_at: '2025-03-05T08:00:00Z',
  },
]

const demoContacts: DemoContact[] = [
  { id: 1, customerId: 1, name: '林志偉', title: '資訊部經理', email: 'lin@twtech.com', phone: '02-1234-5678#101', mobile: '0912-345-678', is_primary: true, notes: '主要對接窗口', created_at: '2024-01-15T08:00:00Z' },
  { id: 2, customerId: 1, name: '黃美玲', title: '採購主管', email: 'huang@twtech.com', phone: '02-1234-5678#202', mobile: '0923-456-789', is_primary: false, notes: '', created_at: '2024-02-10T08:00:00Z' },
  { id: 3, customerId: 2, name: '陳建宏', title: '副總經理', email: 'chen@dazhong.com', phone: '02-2345-6789#301', mobile: '0934-567-890', is_primary: true, notes: '決策者', created_at: '2024-03-20T10:00:00Z' },
  { id: 4, customerId: 3, name: '王大明', title: '廠長', email: 'wang@yongfeng.com', phone: '04-3456-7890#100', mobile: '0945-678-901', is_primary: true, notes: '技術對接', created_at: '2024-05-10T14:00:00Z' },
  { id: 5, customerId: 3, name: '劉雅琪', title: 'IT 主任', email: 'liu@yongfeng.com', phone: '04-3456-7890#105', mobile: '0956-789-012', is_primary: false, notes: '', created_at: '2024-06-01T08:00:00Z' },
  { id: 6, customerId: 4, name: '張家豪', title: '執行長', email: 'zhang@newdigital.com', phone: '02-4567-8901', mobile: '0967-890-123', is_primary: true, notes: '', created_at: '2024-07-01T09:00:00Z' },
  { id: 7, customerId: 5, name: '李明哲', title: '研發部博士', email: 'li@greentech.com', phone: '03-5678-9012#200', mobile: '0978-901-234', is_primary: true, notes: '', created_at: '2024-08-15T11:00:00Z' },
  { id: 8, customerId: 6, name: '趙國棟', title: '資訊長', email: 'zhao@dingxin.com', phone: '02-6789-0123#500', mobile: '0911-234-567', is_primary: true, notes: '高階主管', created_at: '2024-02-10T08:00:00Z' },
  { id: 9, customerId: 6, name: '孫佳蓉', title: '專案經理', email: 'sun@dingxin.com', phone: '02-6789-0123#501', mobile: '0922-345-678', is_primary: false, notes: '日常聯繫窗口', created_at: '2024-03-01T08:00:00Z' },
  { id: 10, customerId: 7, name: '周志遠', title: '營運經理', email: 'zhou@bhmart.com', phone: '07-7890-1234#110', mobile: '0933-456-789', is_primary: true, notes: '', created_at: '2024-09-05T08:00:00Z' },
  { id: 11, customerId: 8, name: '吳佩珊', title: '業務總監', email: 'wu@hongyu.com', phone: '02-8901-2345#300', mobile: '0944-567-890', is_primary: true, notes: '', created_at: '2024-04-18T08:00:00Z' },
  { id: 12, customerId: 8, name: '鄭凱文', title: '物流經理', email: 'zheng@hongyu.com', phone: '02-8901-2345#301', mobile: '0955-678-901', is_primary: false, notes: '物流系統對接', created_at: '2024-05-01T08:00:00Z' },
  { id: 13, customerId: 9, name: '何宗翰', title: '總經理', email: 'he@smartmfg.com', phone: '03-9012-3456', mobile: '0966-789-012', is_primary: true, notes: '', created_at: '2025-01-10T08:00:00Z' },
  { id: 14, customerId: 10, name: '蔡欣妤', title: '製作人', email: 'tsai@quickshot.tw', phone: '02-0123-4567', mobile: '0977-890-123', is_primary: true, notes: '', created_at: '2025-02-01T08:00:00Z' },
]

export function useDemoCustomers() {
  const customers = ref<DemoCustomer[]>(demoCustomers)
  const contacts = ref<DemoContact[]>(demoContacts)

  function findById(id: number) {
    return customers.value.find(c => c.id === id) ?? null
  }

  function findContactById(id: number) {
    return contacts.value.find(c => c.id === id) ?? null
  }

  function getCustomerContacts(customerId: number) {
    return contacts.value.filter(c => c.customerId === customerId)
  }

  function getPrimaryContact(customerId: number) {
    return contacts.value.find(c => c.customerId === customerId && c.is_primary) ?? null
  }

  function getCustomerCountByLevel() {
    const levels: CustomerLevel[] = ['VIP', '一般', '潛在']
    const counts = levels.map(level => ({
      level,
      count: customers.value.filter(c => c.level === level).length,
    }))
    const total = customers.value.length
    return { counts, total }
  }

  function getCustomerCountByIndustry() {
    const industries: CustomerIndustry[] = ['資訊科技', '國際貿易', '製造業', '數位媒體', '環保科技', '金融業', '零售業', '其他']
    return industries
      .map(industry => ({
        industry,
        count: customers.value.filter(c => c.industry === industry).length,
      }))
      .filter(item => item.count > 0)
  }

  function getRecentCustomers(limit: number) {
    return [...customers.value]
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at))
      .slice(0, limit)
  }

  return {
    customers,
    contacts,
    findById,
    findContactById,
    getCustomerContacts,
    getPrimaryContact,
    getCustomerCountByLevel,
    getCustomerCountByIndustry,
    getRecentCustomers,
  }
}
