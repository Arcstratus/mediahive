<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoRole } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { roles } = useDemoRoles()

const columns: TableColumn<DemoRole>[] = [
  { accessorKey: 'name', header: '角色名稱' },
  { accessorKey: 'description', header: '說明' },
  { accessorKey: 'userCount', header: '使用者數' },
  { id: 'permissions', header: '權限' },
  { accessorKey: 'created_at', header: '建立時間' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '角色權限' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">角色權限</h1>
      <UButton label="新增角色" icon="i-lucide-plus" to="/role/new" />
    </div>

    <UTable :data="roles" :columns="columns">
      <template #permissions-cell="{ row }">
        <div class="flex gap-1 flex-wrap">
          <UBadge v-for="perm in row.original.permissions" :key="perm" :label="perm" variant="subtle" size="xs" />
        </div>
      </template>
      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>
      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton icon="i-lucide-pencil" variant="ghost" color="neutral" size="xs" :to="`/role/${row.original.id}`" />
        </div>
      </template>
    </UTable>
  </div>
</template>
