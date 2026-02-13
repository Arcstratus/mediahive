<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface LogisticsItem {
  id: number
  shipmentNo: string
  customer: string
  address: string
  status: string
  shipped_at: string
}

// TODO: 後端支援 - 從 API 取得物流配送資料
const items = ref<LogisticsItem[]>([
  { id: 1, shipmentNo: 'SH-20250101', customer: '台積電股份有限公司', address: '新竹市新竹科學園區力行路 8 號', status: '已送達', shipped_at: '2025-01-10T07:30:00Z' },
  { id: 2, shipmentNo: 'SH-20250102', customer: '鴻海精密工業', address: '新北市土城區自由街 2 號', status: '運送中', shipped_at: '2025-01-09T14:00:00Z' },
  { id: 3, shipmentNo: 'SH-20250103', customer: '聯發科技', address: '新竹市篤行路 1 號', status: '準備中', shipped_at: '2025-01-08T09:45:00Z' },
  { id: 4, shipmentNo: 'SH-20250104', customer: '廣達電腦', address: '桃園市龜山區文化二路 211 號', status: '運送中', shipped_at: '2025-01-07T11:20:00Z' },
  { id: 5, shipmentNo: 'SH-20250105', customer: '華碩電腦', address: '台北市北投區立德路 15 號', status: '已送達', shipped_at: '2025-01-06T08:00:00Z' },
])

const columns: TableColumn<LogisticsItem>[] = [
  { accessorKey: 'shipmentNo', header: '出貨單號' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'address', header: '配送地址' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'shipped_at', header: '出貨時間' },
]

const statusColorMap: Record<string, string> = {
  '準備中': 'warning',
  '運送中': 'info',
  '已送達': 'success',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'ERP', to: '/erp' }, { label: '物流配送' }]" />

    <h1 class="text-2xl font-bold">物流配送</h1>

    <UTable :data="items" :columns="columns">
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(statusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #shipped_at-cell="{ row }">
        {{ formatDate(row.original.shipped_at) }}
      </template>
    </UTable>
  </div>
</template>
