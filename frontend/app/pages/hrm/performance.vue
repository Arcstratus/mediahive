<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface PerformanceItem {
  id: number
  employee: string
  period: string
  kpi_rate: string
  grade: 'A' | 'B' | 'C' | 'D'
  comment: string
}

// TODO: 後端支援 - 從 API 取得績效考核資料
const items = ref<PerformanceItem[]>([
  { id: 1, employee: '陳大文', period: '2024 H2', kpi_rate: '95%', grade: 'A', comment: '表現優異，主導多項專案順利上線' },
  { id: 2, employee: '林小美', period: '2024 H2', kpi_rate: '88%', grade: 'B', comment: '工作態度積極，溝通協調能力佳' },
  { id: 3, employee: '王志明', period: '2024 H2', kpi_rate: '92%', grade: 'A', comment: '業績達標率高，客戶滿意度優良' },
  { id: 4, employee: '張雅婷', period: '2024 H2', kpi_rate: '75%', grade: 'C', comment: '需加強時間管理，報表偶有延遲' },
  { id: 5, employee: '李國華', period: '2024 H2', kpi_rate: '90%', grade: 'B', comment: '技術能力突出，建議加強跨部門合作' },
])

const columns: TableColumn<PerformanceItem>[] = [
  { accessorKey: 'employee', header: '員工' },
  { accessorKey: 'period', header: '考核期間' },
  { accessorKey: 'kpi_rate', header: 'KPI 達成率' },
  { id: 'grade', accessorKey: 'grade', header: '評等' },
  { accessorKey: 'comment', header: '主管評語' },
]

function getGradeColor(grade: PerformanceItem['grade']) {
  switch (grade) {
    case 'A': return 'success'
    case 'B': return 'info'
    case 'C': return 'warning'
    case 'D': return 'error'
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM', to: '/hrm' }, { label: '績效考核' }]" />

    <h1 class="text-2xl font-bold">績效考核</h1>

    <UTable :data="items" :columns="columns">
      <template #grade-cell="{ row }">
        <UBadge
          :label="row.original.grade"
          :color="getGradeColor(row.original.grade)"
          variant="subtle"
          size="sm"
        />
      </template>
    </UTable>
  </div>
</template>
