<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const stats = [
  { label: '本月營收', value: 'NT$ 2,450,000', icon: 'i-lucide-dollar-sign', color: 'text-green-500' },
  { label: '新增客戶', value: '12 家', icon: 'i-lucide-user-plus', color: 'text-blue-500' },
  { label: '成交商機', value: '8 筆', icon: 'i-lucide-trophy', color: 'text-yellow-500' },
  { label: '客服滿意度', value: '94.5%', icon: 'i-lucide-smile', color: 'text-purple-500' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'CRM', to: '/crm' }, { label: '報表分析' }]" />

    <h1 class="text-2xl font-bold">報表分析</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <UCard v-for="stat in stats" :key="stat.label">
        <div class="flex items-center gap-4">
          <UIcon :name="stat.icon" :class="['size-10 shrink-0', stat.color]" />
          <div>
            <p class="text-sm text-muted">{{ stat.label }}</p>
            <p class="text-2xl font-bold">{{ stat.value }}</p>
          </div>
        </div>
      </UCard>
    </div>

    <UCard>
      <div class="flex flex-col items-center justify-center py-12 text-muted">
        <UIcon name="i-lucide-chart-bar" class="size-12 mb-3" />
        <p class="text-lg">圖表區域 - 即將推出</p>
      </div>
    </UCard>
  </div>
</template>
