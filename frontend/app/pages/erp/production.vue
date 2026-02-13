<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface ProductionItem {
  id: number
  workOrderNo: string
  product: string
  quantity: number
  dueDate: string
  status: string
  created_at: string
}

// TODO: 後端支援 - 從 API 取得生產工單資料
const items = ref<ProductionItem[]>([
  { id: 1, workOrderNo: 'WO-20250101', product: '主機板 A 型', quantity: 500, dueDate: '2025-02-15T00:00:00Z', status: '生產中', created_at: '2025-01-10T08:00:00Z' },
  { id: 2, workOrderNo: 'WO-20250102', product: '電源供應器 650W', quantity: 300, dueDate: '2025-02-20T00:00:00Z', status: '排程中', created_at: '2025-01-09T10:30:00Z' },
  { id: 3, workOrderNo: 'WO-20250103', product: '散熱模組 Pro', quantity: 1000, dueDate: '2025-01-30T00:00:00Z', status: '已完成', created_at: '2025-01-08T14:00:00Z' },
  { id: 4, workOrderNo: 'WO-20250104', product: '機殼 ATX 標準型', quantity: 200, dueDate: '2025-03-01T00:00:00Z', status: '排程中', created_at: '2025-01-07T09:15:00Z' },
  { id: 5, workOrderNo: 'WO-20250105', product: '記憶體模組 DDR5', quantity: 800, dueDate: '2025-02-28T00:00:00Z', status: '生產中', created_at: '2025-01-06T11:45:00Z' },
])

const columns: TableColumn<ProductionItem>[] = [
  { accessorKey: 'workOrderNo', header: '工單編號' },
  { accessorKey: 'product', header: '產品' },
  { accessorKey: 'quantity', header: '數量' },
  { accessorKey: 'dueDate', header: '預計完成日' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'created_at', header: '建立時間' },
]

const statusColorMap: Record<string, string> = {
  '排程中': 'warning',
  '生產中': 'info',
  '已完成': 'success',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'ERP', to: '/erp' }, { label: '生產製造' }]" />

    <h1 class="text-2xl font-bold">生產製造</h1>

    <UTable :data="items" :columns="columns">
      <template #dueDate-cell="{ row }">
        {{ formatDate(row.original.dueDate) }}
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
