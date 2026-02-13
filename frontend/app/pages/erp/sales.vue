<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface SalesItem {
  id: number
  orderNo: string
  customer: string
  itemCount: number
  amount: number
  status: string
  created_at: string
}

// TODO: 後端支援 - 從 API 取得銷售資料
const items = ref<SalesItem[]>([
  { id: 1, orderNo: 'SO-20250201', customer: '台積電股份有限公司', itemCount: 10, amount: 520000, status: '已完成', created_at: '2025-01-10T09:00:00Z' },
  { id: 2, orderNo: 'SO-20250202', customer: '鴻海精密工業', itemCount: 4, amount: 186000, status: '已出貨', created_at: '2025-01-09T13:30:00Z' },
  { id: 3, orderNo: 'SO-20250203', customer: '聯發科技', itemCount: 7, amount: 345000, status: '處理中', created_at: '2025-01-08T10:45:00Z' },
  { id: 4, orderNo: 'SO-20250204', customer: '廣達電腦', itemCount: 2, amount: 92000, status: '處理中', created_at: '2025-01-07T15:20:00Z' },
  { id: 5, orderNo: 'SO-20250205', customer: '華碩電腦', itemCount: 5, amount: 278000, status: '已出貨', created_at: '2025-01-06T08:30:00Z' },
])

const columns: TableColumn<SalesItem>[] = [
  { accessorKey: 'orderNo', header: '訂單編號' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'itemCount', header: '品項數' },
  { accessorKey: 'amount', header: '金額' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'created_at', header: '建立時間' },
]

const statusColorMap: Record<string, string> = {
  '處理中': 'warning',
  '已出貨': 'info',
  '已完成': 'success',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'ERP', to: '/erp' }, { label: '銷售管理' }]" />

    <h1 class="text-2xl font-bold">銷售管理</h1>

    <UTable :data="items" :columns="columns">
      <template #amount-cell="{ row }">
        {{ row.original.amount.toLocaleString() }}
      </template>
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>
    </UTable>
  </div>
</template>
