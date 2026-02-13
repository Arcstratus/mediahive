<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得專案資料
const project = {
  id,
  name: 'ERP 系統導入',
  customer: '台灣科技股份有限公司',
  manager: '陳大文',
  start_date: '2025-01-01',
  end_date: '2025-06-30',
  progress: 35,
  status: '進行中',
  description: '為客戶導入完整 ERP 系統，包含庫存、採購、銷售及財務模組。',
}

const statusColorMap: Record<string, string> = {
  '規劃中': 'neutral',
  '進行中': 'info',
  '已完成': 'success',
  '已暫停': 'warning',
  '已取消': 'error',
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name },
    ]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">{{ project.name }}</h1>
      <div class="flex gap-2">
        <UBadge
          :label="project.status"
          :color="(statusColorMap[project.status] as any) ?? 'neutral'"
          variant="subtle"
        />
        <UButton label="編輯" icon="i-lucide-pencil" variant="outline" :to="`/project/${id}/edit`" />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">專案資訊</h3>
        </template>
        <dl class="flex flex-col gap-3">
          <div class="flex justify-between">
            <dt class="text-muted">客戶</dt>
            <dd>{{ project.customer }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">專案經理</dt>
            <dd>{{ project.manager }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">開始日期</dt>
            <dd>{{ formatDate(project.start_date) }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">結束日期</dt>
            <dd>{{ formatDate(project.end_date) }}</dd>
          </div>
        </dl>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">進度</h3>
        </template>
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-4">
            <UProgress :value="project.progress" size="lg" class="flex-1" />
            <span class="text-lg font-bold">{{ project.progress }}%</span>
          </div>
          <p class="text-sm text-muted">{{ project.description }}</p>
        </div>
      </UCard>
    </div>
  </div>
</template>
