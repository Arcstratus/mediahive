<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoCustomer } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { customers } = useDemoCustomers()

const columns: TableColumn<DemoCustomer>[] = [
  { accessorKey: 'name', header: '客戶名稱' },
  { accessorKey: 'contact', header: '聯絡人' },
  { accessorKey: 'email', header: '電子郵件' },
  { accessorKey: 'phone', header: '電話' },
  { accessorKey: 'industry', header: '產業' },
  { id: 'level', accessorKey: 'level', header: '等級' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]

const levelColorMap: Record<string, string> = {
  'VIP': 'warning',
  '一般': 'info',
  '潛在': 'neutral',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'CRM', to: '/crm' }, { label: '客戶管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">客戶管理</h1>
      <UButton label="新增客戶" icon="i-lucide-plus" to="/crm/customer/new" />
    </div>

    <UTable :data="customers" :columns="columns">
      <template #level-cell="{ row }">
        <UBadge
          :label="row.original.level"
          :color="(levelColorMap[row.original.level] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status === 'active' ? '啟用' : '停用'"
          :color="row.original.status === 'active' ? 'success' : 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/crm/customer/${row.original.id}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
