<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface QuoteItem {
  id: number
  quoteNo: string
  customer: string
  itemCount: number
  amount: number
  status: string
  valid_until: string
  created_at: string
}

// TODO: 後端支援 - 從 API 取得報價資料
const items = ref<QuoteItem[]>([
  { id: 1, quoteNo: 'QT-20250101', customer: '台灣科技股份有限公司', itemCount: 5, amount: 680000, status: '已報價', valid_until: '2025-03-31', created_at: '2025-01-15T09:00:00Z' },
  { id: 2, quoteNo: 'QT-20250102', customer: '大眾貿易有限公司', itemCount: 3, amount: 245000, status: '草稿', valid_until: '2025-04-15', created_at: '2025-01-14T10:30:00Z' },
  { id: 3, quoteNo: 'QT-20250103', customer: '永豐製造股份有限公司', itemCount: 8, amount: 1120000, status: '已接受', valid_until: '2025-02-28', created_at: '2025-01-12T14:00:00Z' },
  { id: 4, quoteNo: 'QT-20250104', customer: '新創數位有限公司', itemCount: 2, amount: 156000, status: '已報價', valid_until: '2025-04-30', created_at: '2025-01-10T11:15:00Z' },
  { id: 5, quoteNo: 'QT-20250105', customer: '綠能環保科技公司', itemCount: 6, amount: 890000, status: '已過期', valid_until: '2025-01-01', created_at: '2024-12-01T08:45:00Z' },
])

const columns: TableColumn<QuoteItem>[] = [
  { accessorKey: 'quoteNo', header: '報價單號' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'itemCount', header: '品項數' },
  { id: 'amount', accessorKey: 'amount', header: '金額' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'valid_until', header: '有效期限' },
  { accessorKey: 'created_at', header: '建立時間' },
  { id: 'actions', header: '' },
]

const statusColorMap: Record<string, string> = {
  '草稿': 'neutral',
  '已報價': 'info',
  '已接受': 'success',
  '已拒絕': 'error',
  '已過期': 'warning',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '報價管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">報價管理</h1>
      <UButton label="新增報價" icon="i-lucide-plus" to="/quote/new" />
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

      <template #valid_until-cell="{ row }">
        {{ formatDate(row.original.valid_until) }}
      </template>

      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/quote/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
