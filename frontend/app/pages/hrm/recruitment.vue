<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface RecruitmentItem {
  id: number
  position: string
  department: string
  applicants: number
  interviewing: number
  status: '招募中' | '已錄取' | '已關閉'
}

// TODO: 後端支援 - 從 API 取得招募資料
const items = ref<RecruitmentItem[]>([
  { id: 1, position: '前端工程師', department: '資訊部', applicants: 42, interviewing: 5, status: '招募中' },
  { id: 2, position: '人資助理', department: '人資部', applicants: 28, interviewing: 3, status: '招募中' },
  { id: 3, position: '業務代表', department: '業務部', applicants: 35, interviewing: 0, status: '已錄取' },
  { id: 4, position: '財務分析師', department: '財務部', applicants: 19, interviewing: 2, status: '招募中' },
  { id: 5, position: '後端工程師', department: '研發部', applicants: 56, interviewing: 0, status: '已關閉' },
])

const columns: TableColumn<RecruitmentItem>[] = [
  { accessorKey: 'position', header: '職缺名稱' },
  { accessorKey: 'department', header: '部門' },
  { accessorKey: 'applicants', header: '應徵人數' },
  { accessorKey: 'interviewing', header: '面試中' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
]

function getStatusColor(status: RecruitmentItem['status']) {
  switch (status) {
    case '招募中': return 'info'
    case '已錄取': return 'success'
    case '已關閉': return 'neutral'
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM', to: '/hrm' }, { label: '招募管理' }]" />

    <h1 class="text-2xl font-bold">招募管理</h1>

    <UTable :data="items" :columns="columns">
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
