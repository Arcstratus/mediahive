<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface TrainingItem {
  id: number
  course: string
  instructor: string
  date: string
  hours: number
  participants: number
  status: '規劃中' | '進行中' | '已完成'
}

// TODO: 後端支援 - 從 API 取得教育訓練資料
const items = ref<TrainingItem[]>([
  { id: 1, course: '資訊安全基礎認知', instructor: '陳教授', date: '2024-12-15', hours: 8, participants: 25, status: '已完成' },
  { id: 2, course: '專案管理實務', instructor: '林顧問', date: '2025-01-10', hours: 16, participants: 18, status: '進行中' },
  { id: 3, course: '溝通與簡報技巧', instructor: '王講師', date: '2025-02-20', hours: 6, participants: 30, status: '規劃中' },
  { id: 4, course: 'Python 資料分析入門', instructor: '張工程師', date: '2024-11-25', hours: 24, participants: 12, status: '已完成' },
  { id: 5, course: '領導力與團隊建設', instructor: '李經理', date: '2025-03-05', hours: 12, participants: 15, status: '規劃中' },
])

const columns: TableColumn<TrainingItem>[] = [
  { accessorKey: 'course', header: '課程名稱' },
  { accessorKey: 'instructor', header: '講師' },
  { accessorKey: 'date', header: '日期' },
  { accessorKey: 'hours', header: '時數' },
  { accessorKey: 'participants', header: '參加人數' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
]

function getStatusColor(status: TrainingItem['status']) {
  switch (status) {
    case '規劃中': return 'warning'
    case '進行中': return 'info'
    case '已完成': return 'success'
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM', to: '/hrm' }, { label: '教育訓練' }]" />

    <h1 class="text-2xl font-bold">教育訓練</h1>

    <UTable :data="items" :columns="columns">
      <template #date-cell="{ row }">
        {{ formatDate(row.original.date) }}
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
