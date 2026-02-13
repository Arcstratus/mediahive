<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface ContractItem {
  id: number
  contract_no: string
  customer: string
  amount: string
  start_date: string
  end_date: string
  status: string
}

// TODO: 後端支援 - 從 API 取得合約資料
const items = ref<ContractItem[]>([
  { id: 1, contract_no: 'CTR-2024-001', customer: '台灣科技股份有限公司', amount: 'NT$ 1,200,000', start_date: '2024-01-01', end_date: '2024-12-31', status: '有效' },
  { id: 2, contract_no: 'CTR-2024-002', customer: '大眾貿易有限公司', amount: 'NT$ 360,000', start_date: '2024-03-01', end_date: '2025-02-28', status: '有效' },
  { id: 3, contract_no: 'CTR-2023-015', customer: '永豐製造股份有限公司', amount: 'NT$ 720,000', start_date: '2023-06-01', end_date: '2024-05-31', status: '即將到期' },
  { id: 4, contract_no: 'CTR-2023-008', customer: '新創數位有限公司', amount: 'NT$ 180,000', start_date: '2023-01-01', end_date: '2023-12-31', status: '已到期' },
  { id: 5, contract_no: 'CTR-2024-003', customer: '綠能環保科技公司', amount: 'NT$ 2,500,000', start_date: '2024-04-01', end_date: '2026-03-31', status: '有效' },
])

const columns: TableColumn<ContractItem>[] = [
  { accessorKey: 'contract_no', header: '合約編號' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'amount', header: '金額' },
  { accessorKey: 'start_date', header: '起始日' },
  { accessorKey: 'end_date', header: '到期日' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
]

const statusColorMap: Record<string, string> = {
  '有效': 'success',
  '即將到期': 'warning',
  '已到期': 'error',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '合約管理' }]" />

    <h1 class="text-2xl font-bold">合約管理</h1>

    <UTable :data="items" :columns="columns">
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #start_date-cell="{ row }">
        {{ formatDate(row.original.start_date) }}
      </template>

      <template #end_date-cell="{ row }">
        {{ formatDate(row.original.end_date) }}
      </template>
    </UTable>
  </div>
</template>
