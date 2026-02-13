import type { DemoCustomer } from '~/types'

// TODO: 後端支援 - 改為從 API 取得客戶資料
const demoCustomers: DemoCustomer[] = [
  { id: 1, name: '台灣科技股份有限公司', contact: '林經理', email: 'lin@twtech.com', phone: '02-1234-5678', industry: '資訊科技', level: 'VIP', status: 'active', created_at: '2024-01-15T08:00:00Z' },
  { id: 2, name: '大眾貿易有限公司', contact: '陳副總', email: 'chen@dazhong.com', phone: '02-2345-6789', industry: '國際貿易', level: '一般', status: 'active', created_at: '2024-03-20T10:00:00Z' },
  { id: 3, name: '永豐製造股份有限公司', contact: '王廠長', email: 'wang@yongfeng.com', phone: '04-3456-7890', industry: '製造業', level: '一般', status: 'active', created_at: '2024-05-10T14:00:00Z' },
  { id: 4, name: '新創數位有限公司', contact: '張執行長', email: 'zhang@newdigital.com', phone: '02-4567-8901', industry: '數位媒體', level: '潛在', status: 'active', created_at: '2024-07-01T09:00:00Z' },
  { id: 5, name: '綠能環保科技公司', contact: '李博士', email: 'li@greentech.com', phone: '03-5678-9012', industry: '環保科技', level: '潛在', status: 'inactive', created_at: '2024-08-15T11:00:00Z' },
]

export function useDemoCustomers() {
  const customers = ref<DemoCustomer[]>(demoCustomers)
  function findById(id: number) { return customers.value.find(c => c.id === id) ?? null }
  return { customers, findById }
}
