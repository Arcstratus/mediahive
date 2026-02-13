<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoEmployee } from '~/types'

definePageMeta({ layout: 'dashboard' })
const { employees } = useDemoEmployees()

const columns: TableColumn<DemoEmployee>[] = [
  { accessorKey: 'name', header: '姓名' },
  { accessorKey: 'department', header: '部門' },
  { accessorKey: 'position', header: '職位' },
  { accessorKey: 'email', header: '電子郵件' },
  { accessorKey: 'phone', header: '電話' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'hire_date', header: '到職日' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM', to: '/hrm' }, { label: '員工管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">員工管理</h1>
      <UButton label="新增員工" icon="i-lucide-plus" to="/hrm/employee/new" />
    </div>

    <UTable :data="employees" :columns="columns">
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status === 'active' ? '啟用' : '停用'"
          :color="row.original.status === 'active' ? 'success' : 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #hire_date-cell="{ row }">
        {{ formatDate(row.original.hire_date) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/hrm/employee/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
