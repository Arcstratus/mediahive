<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface CampaignItem {
  id: number
  name: string
  type: string
  budget: string
  start_date: string
  status: string
  conversion_rate: string
}

// TODO: 後端支援 - 從 API 取得行銷活動資料
const items = ref<CampaignItem[]>([
  { id: 1, name: '春季產品發表會', type: '線下', budget: 'NT$ 300,000', start_date: '2024-03-15', status: '已結束', conversion_rate: '12.5%' },
  { id: 2, name: 'Facebook 廣告投放', type: '社群', budget: 'NT$ 150,000', start_date: '2024-05-01', status: '進行中', conversion_rate: '8.3%' },
  { id: 3, name: '線上研討會 - AI 趨勢', type: '線上', budget: 'NT$ 50,000', start_date: '2024-06-20', status: '進行中', conversion_rate: '15.2%' },
  { id: 4, name: '年中促銷 EDM', type: '線上', budget: 'NT$ 80,000', start_date: '2024-07-01', status: '規劃中', conversion_rate: '-' },
  { id: 5, name: '產業博覽會參展', type: '線下', budget: 'NT$ 500,000', start_date: '2024-09-10', status: '規劃中', conversion_rate: '-' },
])

const columns: TableColumn<CampaignItem>[] = [
  { accessorKey: 'name', header: '活動名稱' },
  { id: 'type', accessorKey: 'type', header: '類型' },
  { accessorKey: 'budget', header: '預算' },
  { accessorKey: 'start_date', header: '開始日期' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'conversion_rate', header: '轉換率' },
]

const typeColorMap: Record<string, string> = {
  '線上': 'info',
  '線下': 'warning',
  '社群': 'success',
}

const statusColorMap: Record<string, string> = {
  '規劃中': 'neutral',
  '進行中': 'success',
  '已結束': 'info',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '行銷活動' }]" />

    <h1 class="text-2xl font-bold">行銷活動</h1>

    <UTable :data="items" :columns="columns">
      <template #type-cell="{ row }">
        <UBadge
          :label="row.original.type"
          :color="(typeColorMap[row.original.type] as any) ?? 'neutral'"
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

      <template #start_date-cell="{ row }">
        {{ formatDate(row.original.start_date) }}
      </template>
    </UTable>
  </div>
</template>
