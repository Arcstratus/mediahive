<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

// TODO: 後端支援 - 從 API 取得通知範本列表
interface NotificationTemplate {
  id: number
  name: string
  channel: string
  event: string
  enabled: boolean
  updated_at: string
}

const templates = ref<NotificationTemplate[]>([
  { id: 1, name: '歡迎信', channel: 'Email', event: '使用者註冊', enabled: true, updated_at: '2025-05-01T10:00:00Z' },
  { id: 2, name: '密碼重設', channel: 'Email', event: '密碼重設請求', enabled: true, updated_at: '2025-05-01T10:00:00Z' },
  { id: 3, name: '新資源通知', channel: '站內通知', event: '資源上傳完成', enabled: true, updated_at: '2025-05-10T14:00:00Z' },
  { id: 4, name: '系統維護公告', channel: 'Email', event: '系統維護排程', enabled: false, updated_at: '2025-05-15T08:00:00Z' },
  { id: 5, name: '備份完成通知', channel: '站內通知', event: '排程備份完成', enabled: true, updated_at: '2025-05-20T16:00:00Z' },
])

const columns: TableColumn<NotificationTemplate>[] = [
  { accessorKey: 'name', header: '範本名稱' },
  { accessorKey: 'channel', header: '通知管道' },
  { accessorKey: 'event', header: '觸發事件' },
  { id: 'enabled', accessorKey: 'enabled', header: '狀態' },
  { accessorKey: 'updated_at', header: '更新時間' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Foundation', to: '/foundation' }, { label: '通知中心' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">通知中心</h1>
    </div>

    <UTable :data="templates" :columns="columns">
      <template #enabled-cell="{ row }">
        <UBadge
          :label="row.original.enabled ? '啟用' : '停用'"
          :color="row.original.enabled ? 'success' : 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #updated_at-cell="{ row }">
        {{ formatDate(row.original.updated_at) }}
      </template>
    </UTable>
  </div>
</template>
