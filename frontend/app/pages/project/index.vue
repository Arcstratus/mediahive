<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface ProjectItem {
  id: number
  name: string
  customer: string
  manager: string
  start_date: string
  end_date: string
  progress: number
  status: string
}

// TODO: 後端支援 - 從 API 取得專案資料
const items = ref<ProjectItem[]>([
  { id: 1, name: 'ERP 系統導入', customer: '台灣科技股份有限公司', manager: '陳大文', start_date: '2025-01-01', end_date: '2025-06-30', progress: 35, status: '進行中' },
  { id: 2, name: '官網改版專案', customer: '新創數位有限公司', manager: '林小美', start_date: '2025-02-01', end_date: '2025-04-30', progress: 10, status: '規劃中' },
  { id: 3, name: '雲端遷移服務', customer: '永豐製造股份有限公司', manager: '王志明', start_date: '2024-10-01', end_date: '2025-03-31', progress: 80, status: '進行中' },
  { id: 4, name: '智慧工廠方案', customer: '綠能環保科技公司', manager: '張雅婷', start_date: '2024-08-01', end_date: '2024-12-31', progress: 100, status: '已完成' },
  { id: 5, name: '年度維護合約', customer: '大眾貿易有限公司', manager: '李國華', start_date: '2025-01-01', end_date: '2025-12-31', progress: 5, status: '進行中' },
])

const columns: TableColumn<ProjectItem>[] = [
  { accessorKey: 'name', header: '專案名稱' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'manager', header: '專案經理' },
  { accessorKey: 'start_date', header: '開始日期' },
  { accessorKey: 'end_date', header: '結束日期' },
  { id: 'progress', accessorKey: 'progress', header: '進度' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]

const statusColorMap: Record<string, string> = {
  '規劃中': 'neutral',
  '進行中': 'info',
  '已完成': 'success',
  '已暫停': 'warning',
  '已取消': 'error',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '專案管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">專案管理</h1>
      <UButton label="新增專案" icon="i-lucide-plus" to="/project/new" />
    </div>

    <UTable :data="items" :columns="columns">
      <template #start_date-cell="{ row }">
        {{ formatDate(row.original.start_date) }}
      </template>

      <template #end_date-cell="{ row }">
        {{ formatDate(row.original.end_date) }}
      </template>

      <template #progress-cell="{ row }">
        <div class="flex items-center gap-2">
          <UProgress :value="row.original.progress" size="sm" class="w-20" />
          <span class="text-xs text-muted">{{ row.original.progress }}%</span>
        </div>
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
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
            :to="`/project/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
