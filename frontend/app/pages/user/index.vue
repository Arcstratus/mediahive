<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoUser } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { users } = useDemoUsers()

const columns: TableColumn<DemoUser>[] = [
  { id: 'avatar', header: '', size: 50 },
  { accessorKey: 'name', header: '名稱' },
  { accessorKey: 'email', header: '電子郵件' },
  { accessorKey: 'department', header: '部門' },
  { accessorKey: 'role', header: '角色' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { accessorKey: 'created_at', header: '建立時間' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '使用者管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">使用者管理</h1>
      <UButton label="新增使用者" icon="i-lucide-plus" to="/user/new" />
    </div>

    <UTable :data="users" :columns="columns">
      <template #avatar-cell="{ row }">
        <UAvatar :src="row.original.avatar || undefined" icon="i-lucide-user" size="sm" />
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status === 'active' ? '啟用' : '停用'"
          :color="row.original.status === 'active' ? 'success' : 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/user/${row.original.uuid}`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
