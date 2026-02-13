<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface AttendanceItem {
  id: number
  employee: string
  date: string
  clock_in: string
  clock_out: string
  status: '正常' | '遲到' | '請假' | '缺勤'
}

// TODO: 後端支援 - 從 API 取得出勤資料
const items = ref<AttendanceItem[]>([
  { id: 1, employee: '陳大文', date: '2024-12-09', clock_in: '08:55', clock_out: '18:05', status: '正常' },
  { id: 2, employee: '林小美', date: '2024-12-09', clock_in: '09:15', clock_out: '18:10', status: '遲到' },
  { id: 3, employee: '王志明', date: '2024-12-09', clock_in: '', clock_out: '', status: '請假' },
  { id: 4, employee: '張雅婷', date: '2024-12-09', clock_in: '08:50', clock_out: '18:00', status: '正常' },
  { id: 5, employee: '李國華', date: '2024-12-09', clock_in: '', clock_out: '', status: '缺勤' },
])

const columns: TableColumn<AttendanceItem>[] = [
  { accessorKey: 'employee', header: '員工' },
  { accessorKey: 'date', header: '日期' },
  { accessorKey: 'clock_in', header: '上班打卡' },
  { accessorKey: 'clock_out', header: '下班打卡' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]

function getStatusColor(status: AttendanceItem['status']) {
  switch (status) {
    case '正常': return 'success'
    case '遲到': return 'warning'
    case '請假': return 'info'
    case '缺勤': return 'error'
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '出勤管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">出勤管理</h1>
      <UButton label="新增紀錄" icon="i-lucide-plus" to="/attendance/new" />
    </div>

    <UTable :data="items" :columns="columns">
      <template #clock_in-cell="{ row }">
        {{ row.original.clock_in || '-' }}
      </template>

      <template #clock_out-cell="{ row }">
        {{ row.original.clock_out || '-' }}
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="getStatusColor(row.original.status)"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/attendance/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
