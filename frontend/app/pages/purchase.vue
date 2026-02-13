<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface PurchaseItem {
  id: number
  orderNo: string
  supplier: string
  itemCount: number
  amount: number
  status: string
  created_at: string
}

// TODO: 後端支援 - 從 API 取得採購資料
const items = ref<PurchaseItem[]>([
  { id: 1, orderNo: 'PO-20250101', supplier: '大同資訊股份有限公司', itemCount: 5, amount: 152000, status: '已核准', created_at: '2025-01-10T08:00:00Z' },
  { id: 2, orderNo: 'PO-20250102', supplier: '聯強國際', itemCount: 3, amount: 87500, status: '待審核', created_at: '2025-01-09T10:30:00Z' },
  { id: 3, orderNo: 'PO-20250103', supplier: '全國電子', itemCount: 8, amount: 234000, status: '已完成', created_at: '2025-01-08T14:15:00Z' },
  { id: 4, orderNo: 'PO-20250104', supplier: '震旦行', itemCount: 2, amount: 46000, status: '待審核', created_at: '2025-01-07T09:45:00Z' },
  { id: 5, orderNo: 'PO-20250105', supplier: '捷元電腦', itemCount: 6, amount: 198000, status: '已核准', created_at: '2025-01-06T11:20:00Z' },
])

const columns: TableColumn<PurchaseItem>[] = [
  { accessorKey: 'orderNo', header: '單號' },
  { accessorKey: 'supplier', header: '供應商' },
  { accessorKey: 'itemCount', header: '品項數' },
  { accessorKey: 'amount', header: '金額' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'created_at', header: '建立時間' },
]

const statusColorMap: Record<string, string> = {
  '待審核': 'warning',
  '已核准': 'info',
  '已完成': 'success',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '採購管理' }]" />

    <h1 class="text-2xl font-bold">採購管理</h1>

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
