<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface InventoryItem {
  id: number
  name: string
  spec: string
  quantity: number
  warehouse: string
  status: string
  updated_at: string
}

// TODO: 後端支援 - 從 API 取得庫存資料
const items = ref<InventoryItem[]>([
  { id: 1, name: '筆記型電腦', spec: '14 吋 / 16GB / 512GB SSD', quantity: 45, warehouse: 'A 倉', status: '充足', updated_at: '2025-01-10T09:30:00Z' },
  { id: 2, name: '印表機碳粉', spec: '黑色 / 相容型號 HP-26A', quantity: 8, warehouse: 'B 倉', status: '低庫存', updated_at: '2025-01-09T14:20:00Z' },
  { id: 3, name: 'A4 影印紙', spec: '80 磅 / 每箱 5 包', quantity: 120, warehouse: 'A 倉', status: '充足', updated_at: '2025-01-08T11:00:00Z' },
  { id: 4, name: '螢幕', spec: '27 吋 4K IPS', quantity: 22, warehouse: 'A 倉', status: '充足', updated_at: '2025-01-07T16:45:00Z' },
  { id: 5, name: '鍵盤滑鼠組', spec: '無線 / 中文注音', quantity: 3, warehouse: 'B 倉', status: '低庫存', updated_at: '2025-01-06T10:15:00Z' },
])

const columns: TableColumn<InventoryItem>[] = [
  { accessorKey: 'name', header: '品名' },
  { accessorKey: 'spec', header: '規格' },
  { accessorKey: 'quantity', header: '數量' },
  { accessorKey: 'warehouse', header: '倉庫' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'updated_at', header: '更新時間' },
  { id: 'actions', header: '' },
]

const statusColorMap: Record<string, string> = {
  '充足': 'success',
  '低庫存': 'warning',
  '缺貨': 'error',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '庫存管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">庫存管理</h1>
      <UButton label="新增品項" icon="i-lucide-plus" to="/inventory/new" />
    </div>

    <UTable :data="items" :columns="columns">
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #updated_at-cell="{ row }">
        {{ formatDate(row.original.updated_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/inventory/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
