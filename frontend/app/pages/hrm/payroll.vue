<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({ layout: 'dashboard' })

interface PayrollItem {
  id: number
  employee: string
  month: string
  base_salary: number
  overtime_pay: number
  deductions: number
  net_pay: number
}

// TODO: 後端支援 - 從 API 取得薪資資料
const items = ref<PayrollItem[]>([
  { id: 1, employee: '陳大文', month: '2024-11', base_salary: 55000, overtime_pay: 3200, deductions: 5800, net_pay: 52400 },
  { id: 2, employee: '林小美', month: '2024-11', base_salary: 48000, overtime_pay: 1500, deductions: 4950, net_pay: 44550 },
  { id: 3, employee: '王志明', month: '2024-11', base_salary: 65000, overtime_pay: 0, deductions: 7200, net_pay: 57800 },
  { id: 4, employee: '張雅婷', month: '2024-11', base_salary: 52000, overtime_pay: 2400, deductions: 5440, net_pay: 48960 },
  { id: 5, employee: '李國華', month: '2024-11', base_salary: 72000, overtime_pay: 4800, deductions: 8680, net_pay: 68120 },
])

const columns: TableColumn<PayrollItem>[] = [
  { accessorKey: 'employee', header: '員工' },
  { accessorKey: 'month', header: '月份' },
  { id: 'base_salary', accessorKey: 'base_salary', header: '基本薪資' },
  { id: 'overtime_pay', accessorKey: 'overtime_pay', header: '加班費' },
  { id: 'deductions', accessorKey: 'deductions', header: '扣項' },
  { id: 'net_pay', accessorKey: 'net_pay', header: '實發金額' },
]

function formatTWD(amount: number) {
  return `NT$ ${amount.toLocaleString()}`
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM', to: '/hrm' }, { label: '薪資管理' }]" />

    <h1 class="text-2xl font-bold">薪資管理</h1>

    <UTable :data="items" :columns="columns">
      <template #base_salary-cell="{ row }">
        {{ formatTWD(row.original.base_salary) }}
      </template>

      <template #overtime_pay-cell="{ row }">
        {{ formatTWD(row.original.overtime_pay) }}
      </template>

      <template #deductions-cell="{ row }">
        {{ formatTWD(row.original.deductions) }}
      </template>

      <template #net_pay-cell="{ row }">
        <span class="font-semibold">{{ formatTWD(row.original.net_pay) }}</span>
      </template>
    </UTable>
  </div>
</template>
