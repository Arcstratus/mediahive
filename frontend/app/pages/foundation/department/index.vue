<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoDepartment } from '~/types'
import type { DepartmentTreeNode } from '~/composables/useDemoDepartments'

definePageMeta({ layout: 'dashboard' })

const { departments, tree } = useDemoDepartments()

const tab = ref('list')
const tabs = [
  { label: '列表', value: 'list', icon: 'i-lucide-list' },
  { label: '樹狀圖', value: 'tree', icon: 'i-lucide-git-branch' },
]

const columns: TableColumn<DemoDepartment>[] = [
  { accessorKey: 'name', header: '部門名稱' },
  { accessorKey: 'head', header: '主管' },
  { accessorKey: 'memberCount', header: '成員數' },
  { accessorKey: 'created_at', header: '建立時間' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Foundation', to: '/foundation' }, { label: '組織架構' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">組織架構</h1>
      <UButton label="新增部門" icon="i-lucide-plus" to="/foundation/department/new" />
    </div>

    <UTabs v-model="tab" :items="tabs" />

    <!-- List View -->
    <UTable v-if="tab === 'list'" :data="departments" :columns="columns">
      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>
      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton icon="i-lucide-pencil" variant="ghost" color="neutral" size="xs" :to="`/foundation/department/${row.original.id}`" />
        </div>
      </template>
    </UTable>

    <!-- Tree View -->
    <div v-if="tab === 'tree'" class="space-y-2">
      <DepartmentTreeItem v-for="node in tree" :key="node.department.id" :node="node" :depth="0" />
    </div>
  </div>
</template>
