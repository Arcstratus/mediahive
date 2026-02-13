<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface LeaveItem {
  id: number
  employee: string
  type: '特休' | '病假' | '事假' | '公假' | '婚假'
  start_date: string
  end_date: string
  days: number
  reason: string
  status: '待審核' | '已核准' | '已駁回'
}

// TODO: 後端支援 - 從 API 取得請假資料
const items = ref<LeaveItem[]>([
  { id: 1, employee: '陳大文', type: '特休', start_date: '2025-02-10', end_date: '2025-02-12', days: 3, reason: '家庭旅遊', status: '已核准' },
  { id: 2, employee: '林小美', type: '病假', start_date: '2025-02-05', end_date: '2025-02-05', days: 1, reason: '身體不適', status: '已核准' },
  { id: 3, employee: '王志明', type: '事假', start_date: '2025-02-15', end_date: '2025-02-15', days: 1, reason: '個人事務', status: '待審核' },
  { id: 4, employee: '張雅婷', type: '公假', start_date: '2025-02-20', end_date: '2025-02-21', days: 2, reason: '外部培訓課程', status: '已核准' },
  { id: 5, employee: '李國華', type: '特休', start_date: '2025-03-01', end_date: '2025-03-07', days: 5, reason: '出國旅遊', status: '待審核' },
])

const columns: TableColumn<LeaveItem>[] = [
  { accessorKey: 'employee', header: '員工' },
  { id: 'type', accessorKey: 'type', header: '假別' },
  { accessorKey: 'start_date', header: '開始日期' },
  { accessorKey: 'end_date', header: '結束日期' },
  { accessorKey: 'days', header: '天數' },
  { accessorKey: 'reason', header: '事由' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
]

const typeColorMap: Record<string, string> = {
  '特休': 'info',
  '病假': 'warning',
  '事假': 'neutral',
  '公假': 'success',
  '婚假': 'error',
}

function getStatusColor(status: LeaveItem['status']) {
  switch (status) {
    case '待審核': return 'warning'
    case '已核准': return 'success'
    case '已駁回': return 'error'
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '請假管理' }]" />

    <h1 class="text-2xl font-bold">請假管理</h1>

    <UTable :data="items" :columns="columns">
      <template #type-cell="{ row }">
        <UBadge
          :label="row.original.type"
          :color="(typeColorMap[row.original.type] as any) ?? 'neutral'"
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

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="getStatusColor(row.original.status)"
          variant="subtle"
          size="sm"
        />
      </template>
    </UTable>
  </div>
</template>
