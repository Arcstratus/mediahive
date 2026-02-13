<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface TicketItem {
  id: number
  ticket_no: string
  customer: string
  subject: string
  priority: string
  status: string
  created_at: string
}

// TODO: 後端支援 - 從 API 取得客服工單資料
const items = ref<TicketItem[]>([
  { id: 1, ticket_no: 'TK-2024-0001', customer: '台灣科技股份有限公司', subject: '系統登入異常', priority: '高', status: '處理中', created_at: '2024-06-01T09:30:00Z' },
  { id: 2, ticket_no: 'TK-2024-0002', customer: '大眾貿易有限公司', subject: '報表匯出格式錯誤', priority: '中', status: '待處理', created_at: '2024-06-02T14:15:00Z' },
  { id: 3, ticket_no: 'TK-2024-0003', customer: '永豐製造股份有限公司', subject: '請求新增使用者帳號', priority: '低', status: '已解決', created_at: '2024-05-28T10:00:00Z' },
  { id: 4, ticket_no: 'TK-2024-0004', customer: '新創數位有限公司', subject: 'API 串接技術支援', priority: '中', status: '處理中', created_at: '2024-06-03T11:45:00Z' },
  { id: 5, ticket_no: 'TK-2024-0005', customer: '綠能環保科技公司', subject: '合約到期續約諮詢', priority: '低', status: '已關閉', created_at: '2024-05-20T16:30:00Z' },
])

const columns: TableColumn<TicketItem>[] = [
  { accessorKey: 'ticket_no', header: '工單編號' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'subject', header: '主旨' },
  { id: 'priority', accessorKey: 'priority', header: '優先度' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'created_at', header: '建立時間' },
]

const priorityColorMap: Record<string, string> = {
  '高': 'error',
  '中': 'warning',
  '低': 'neutral',
}

const statusColorMap: Record<string, string> = {
  '待處理': 'warning',
  '處理中': 'info',
  '已解決': 'success',
  '已關閉': 'neutral',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '客服工單' }]" />

    <h1 class="text-2xl font-bold">客服工單</h1>

    <UTable :data="items" :columns="columns">
      <template #priority-cell="{ row }">
        <UBadge
          :label="row.original.priority"
          :color="(priorityColorMap[row.original.priority] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
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
