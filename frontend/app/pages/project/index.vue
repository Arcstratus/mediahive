<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoProject, ProjectStatus } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { projects, getProjectsByStatus } = useDemoProjects()

const view = useState('project-view', () => 'table')
const viewTabs = [
  { label: '表格', value: 'table', icon: 'i-lucide-list' },
  { label: '看板', value: 'kanban', icon: 'i-lucide-kanban' },
]

const statusFilter = ref<ProjectStatus | ''>('')
const managerFilter = ref('')
const search = ref('')

const statusOptions = ['', '規劃中', '進行中', '已暫停', '已完成', '已結案', '已取消']
const managerOptions = computed(() => {
  const managers = [...new Set(projects.value.map(p => p.manager))]
  return ['', ...managers]
})

const filteredProjects = computed(() => {
  return projects.value.filter((p) => {
    if (statusFilter.value && p.status !== statusFilter.value) return false
    if (managerFilter.value && p.manager !== managerFilter.value) return false
    if (search.value) {
      const q = search.value.toLowerCase()
      return p.name.toLowerCase().includes(q) || p.customer.toLowerCase().includes(q) || p.code.toLowerCase().includes(q)
    }
    return true
  })
})

const kanbanColumns = computed(() => {
  const all = getProjectsByStatus()
  if (!statusFilter.value && !managerFilter.value && !search.value) return all
  return all.map(col => ({
    status: col.status,
    projects: col.projects.filter(p => filteredProjects.value.includes(p)),
  }))
})

const columns: TableColumn<DemoProject>[] = [
  { accessorKey: 'code', header: '編號' },
  { accessorKey: 'name', header: '專案名稱' },
  { accessorKey: 'customer', header: '客戶' },
  { accessorKey: 'manager', header: '專案經理' },
  { accessorKey: 'start_date', header: '開始日期' },
  { accessorKey: 'end_date', header: '結束日期' },
  { id: 'progress', accessorKey: 'progress', header: '進度' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '專案管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">專案管理</h1>
      <UButton label="新增專案" icon="i-lucide-plus" to="/project/new" />
    </div>

    <div class="flex flex-wrap items-center justify-between gap-3">
      <div class="flex flex-wrap items-center gap-3">
        <USelectMenu v-model="statusFilter" :items="statusOptions" placeholder="所有狀態" class="w-36" />
        <USelectMenu v-model="managerFilter" :items="managerOptions" placeholder="所有經理" class="w-36" />
        <UInput v-model="search" placeholder="搜尋專案名稱、客戶、編號…" icon="i-lucide-search" class="w-64" />
      </div>
      <UTabs v-model="view" :items="viewTabs" />
    </div>

    <!-- 表格 View -->
    <UTable v-if="view === 'table'" :data="filteredProjects" :columns="columns">
      <template #start_date-cell="{ row }">
        {{ formatDate(row.original.start_date) }}
      </template>
      <template #end_date-cell="{ row }">
        {{ formatDate(row.original.end_date) }}
      </template>
      <template #progress-cell="{ row }">
        <div class="flex items-center gap-2">
          <UProgress :value="row.original.progress" size="sm" class="w-20" />
          <span class="text-xs text-muted">{{ row.original.progress }}%</span>
        </div>
      </template>
      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status"
          :color="(projectStatusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>
      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton icon="i-lucide-eye" variant="ghost" color="neutral" size="xs" :to="`/project/${row.original.id}`" />
        </div>
      </template>
    </UTable>

    <!-- 看板 View -->
    <div v-if="view === 'kanban'" class="flex gap-4 overflow-x-auto pb-4">
      <div
        v-for="col in kanbanColumns"
        :key="col.status"
        class="w-72 flex-shrink-0 flex flex-col gap-3"
      >
        <div class="flex items-center gap-2 px-1">
          <UBadge
            :label="col.status"
            :color="(projectStatusColorMap[col.status] as any) ?? 'neutral'"
            variant="subtle"
            size="sm"
          />
          <span class="text-xs text-muted">({{ col.projects.length }})</span>
        </div>

        <div class="flex flex-col gap-2 min-h-24 rounded-lg bg-elevated p-2">
          <NuxtLink
            v-for="p in col.projects"
            :key="p.id"
            :to="`/project/${p.id}`"
            class="block"
          >
            <UCard class="hover:ring-1 hover:ring-primary transition-all cursor-pointer">
              <div class="flex flex-col gap-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-muted">{{ p.code }}</span>
                  <span class="text-xs text-muted">{{ p.manager }}</span>
                </div>
                <p class="text-sm font-medium">{{ p.name }}</p>
                <p class="text-xs text-muted truncate">{{ p.customer }}</p>
                <div class="flex items-center gap-2">
                  <UProgress :value="p.progress" size="xs" class="flex-1" />
                  <span class="text-xs text-muted">{{ p.progress }}%</span>
                </div>
              </div>
            </UCard>
          </NuxtLink>

          <div v-if="!col.projects.length" class="flex items-center justify-center h-16 text-xs text-muted">
            無專案
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
