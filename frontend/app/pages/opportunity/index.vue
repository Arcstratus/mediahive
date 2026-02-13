<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface OpportunityItem {
  id: number
  name: string
  customer: string
  amount: string
  stage: string
  owner: string
  expected_close: string
}

// TODO: 後端支援 - 從 API 取得商機資料
const items = ref<OpportunityItem[]>([
  { id: 1, name: 'ERP 系統導入專案', customer: '台灣科技股份有限公司', amount: 'NT$ 1,200,000', stage: '報價中', owner: '陳業務', expected_close: '2024-06-30' },
  { id: 2, name: '年度維護合約續約', customer: '大眾貿易有限公司', amount: 'NT$ 360,000', stage: '議價中', owner: '林經理', expected_close: '2024-05-15' },
  { id: 3, name: '雲端遷移服務', customer: '永豐製造股份有限公司', amount: 'NT$ 850,000', stage: '需求確認', owner: '王顧問', expected_close: '2024-08-20' },
  { id: 4, name: '品牌官網改版', customer: '新創數位有限公司', amount: 'NT$ 480,000', stage: '初步接洽', owner: '張業務', expected_close: '2024-09-10' },
  { id: 5, name: '智慧工廠方案', customer: '綠能環保科技公司', amount: 'NT$ 2,500,000', stage: '已成交', owner: '陳業務', expected_close: '2024-04-01' },
])

const columns: TableColumn<OpportunityItem>[] = [
  { accessorKey: 'name', header: '商機名稱' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'amount', header: '預估金額' },
  { id: 'stage', accessorKey: 'stage', header: '階段' },
  { accessorKey: 'owner', header: '負責人' },
  { accessorKey: 'expected_close', header: '預計成交日' },
  { id: 'actions', header: '' },
]

const stageColorMap: Record<string, string> = {
  '初步接洽': 'neutral',
  '需求確認': 'info',
  '報價中': 'warning',
  '議價中': 'warning',
  '已成交': 'success',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '商機管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">商機管理</h1>
      <UButton label="新增商機" icon="i-lucide-plus" to="/opportunity/new" />
    </div>

    <UTable :data="items" :columns="columns">
      <template #stage-cell="{ row }">
        <UBadge
          :label="row.original.stage"
          :color="(stageColorMap[row.original.stage] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #expected_close-cell="{ row }">
        {{ formatDate(row.original.expected_close) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton icon="i-lucide-pencil" variant="ghost" color="neutral" size="xs" :to="`/opportunity/${row.original.id}`" />
        </div>
      </template>
    </UTable>
  </div>
</template>
