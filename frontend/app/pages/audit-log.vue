<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoAuditLog } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { logs } = useDemoAuditLogs()

const columns: TableColumn<DemoAuditLog>[] = [
  { accessorKey: 'user', header: '操作者' },
  { id: 'action', accessorKey: 'action', header: '動作' },
  { accessorKey: 'target', header: '對象' },
  { accessorKey: 'detail', header: '詳細說明' },
  { accessorKey: 'ip', header: 'IP 位址' },
  { accessorKey: 'created_at', header: '時間' },
]

const actionColorMap: Record<string, string> = {
  '登入': 'info',
  '新增': 'success',
  '修改': 'warning',
  '刪除': 'error',
  '匯出': 'neutral',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '稽核日誌' }]" />

    <h1 class="text-2xl font-bold">稽核日誌</h1>

    <UTable :data="logs" :columns="columns">
      <template #action-cell="{ row }">
        <UBadge
          :label="row.original.action"
          :color="(actionColorMap[row.original.action] as any) ?? 'neutral'"
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
