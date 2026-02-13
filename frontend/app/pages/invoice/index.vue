<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface InvoiceItem {
  id: number
  invoiceNo: string
  customer: string
  amount: number
  issue_date: string
  due_date: string
  status: string
}

// TODO: 後端支援 - 從 API 取得請款資料
const items = ref<InvoiceItem[]>([
  { id: 1, invoiceNo: 'INV-20250101', customer: '台灣科技股份有限公司', amount: 680000, issue_date: '2025-01-15', due_date: '2025-02-15', status: '已付款' },
  { id: 2, invoiceNo: 'INV-20250102', customer: '大眾貿易有限公司', amount: 245000, issue_date: '2025-01-20', due_date: '2025-02-20', status: '待付款' },
  { id: 3, invoiceNo: 'INV-20250103', customer: '永豐製造股份有限公司', amount: 1120000, issue_date: '2025-01-10', due_date: '2025-02-10', status: '逾期' },
  { id: 4, invoiceNo: 'INV-20250104', customer: '新創數位有限公司', amount: 156000, issue_date: '2025-01-25', due_date: '2025-02-25', status: '待付款' },
  { id: 5, invoiceNo: 'INV-20250105', customer: '綠能環保科技公司', amount: 890000, issue_date: '2025-01-05', due_date: '2025-02-05', status: '已付款' },
])

const columns: TableColumn<InvoiceItem>[] = [
  { accessorKey: 'invoiceNo', header: '請款單號' },
  { accessorKey: 'customer', header: '客戶' },
  { id: 'amount', accessorKey: 'amount', header: '金額' },
  { accessorKey: 'issue_date', header: '開立日期' },
  { accessorKey: 'due_date', header: '付款期限' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]

const statusColorMap: Record<string, string> = {
  '待付款': 'warning',
  '已付款': 'success',
  '逾期': 'error',
  '已取消': 'neutral',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '請款管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">請款管理</h1>
      <UButton label="新增請款" icon="i-lucide-plus" to="/invoice/new" />
    </div>

    <UTable :data="items" :columns="columns">
      <template #amount-cell="{ row }">
        NT$ {{ row.original.amount.toLocaleString() }}
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #issue_date-cell="{ row }">
        {{ formatDate(row.original.issue_date) }}
      </template>

      <template #due_date-cell="{ row }">
        {{ formatDate(row.original.due_date) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/invoice/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
