<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface FinanceItem {
  id: number
  voucherNo: string
  type: string
  account: string
  amount: number
  remark: string
  date: string
}

// TODO: 後端支援 - 從 API 取得財務資料
const items = ref<FinanceItem[]>([
  { id: 1, voucherNo: 'FV-20250101', type: '收入', account: '銷貨收入', amount: 520000, remark: '台積電訂單款項', date: '2025-01-10T00:00:00Z' },
  { id: 2, voucherNo: 'FV-20250102', type: '支出', account: '辦公用品', amount: 15200, remark: '採購文具與耗材', date: '2025-01-09T00:00:00Z' },
  { id: 3, voucherNo: 'FV-20250103', type: '支出', account: '設備折舊', amount: 38000, remark: '一月份設備折舊攤提', date: '2025-01-08T00:00:00Z' },
  { id: 4, voucherNo: 'FV-20250104', type: '收入', account: '利息收入', amount: 4800, remark: '活期存款利息', date: '2025-01-07T00:00:00Z' },
  { id: 5, voucherNo: 'FV-20250105', type: '支出', account: '人事費用', amount: 1250000, remark: '一月份薪資發放', date: '2025-01-06T00:00:00Z' },
])

const columns: TableColumn<FinanceItem>[] = [
  { accessorKey: 'voucherNo', header: '傳票編號' },
  { id: 'type', accessorKey: 'type', header: '類型' },
  { accessorKey: 'account', header: '科目' },
  { accessorKey: 'amount', header: '金額' },
  { accessorKey: 'remark', header: '備註' },
  { accessorKey: 'date', header: '日期' },
]

const typeColorMap: Record<string, string> = {
  '收入': 'success',
  '支出': 'error',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'ERP', to: '/erp' }, { label: '財務會計' }]" />

    <h1 class="text-2xl font-bold">財務會計</h1>

    <UTable :data="items" :columns="columns">
      <template #type-cell="{ row }">
        <UBadge
          :label="row.original.type"
          :color="(typeColorMap[row.original.type] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #amount-cell="{ row }">
        {{ row.original.amount.toLocaleString() }}
      </template>
      <template #date-cell="{ row }">
        {{ formatDate(row.original.date) }}
      </template>
    </UTable>
  </div>
</template>
