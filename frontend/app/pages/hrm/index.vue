<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
})

const features = [
  { title: '員工管理', description: '管理員工基本資料、到職與離職流程', icon: 'i-lucide-user', to: '/hrm/employee' },
  { title: '出勤管理', description: '記錄打卡、請假與加班申請', icon: 'i-lucide-clock', to: '/hrm/attendance' },
  { title: '薪資管理', description: '計算薪資、獎金與扣繳項目', icon: 'i-lucide-banknote', to: '/hrm/payroll' },
  { title: '績效考核', description: '設定 KPI、進行考核與回饋面談', icon: 'i-lucide-trophy', to: '/hrm/performance' },
  { title: '教育訓練', description: '規劃課程、追蹤學習進度與認證', icon: 'i-lucide-graduation-cap', to: '/hrm/training' },
  { title: '招募管理', description: '管理職缺發布、履歷篩選與面試排程', icon: 'i-lucide-briefcase', to: '/hrm/recruitment' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'HRM' }]" />

    <h1 class="text-2xl font-bold">HRM 人力資源管理</h1>
    <p class="text-muted">涵蓋員工、出勤、薪資與績效等人事管理功能。</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <NuxtLink v-for="feature in features" :key="feature.title" :to="feature.to">
        <UCard class="h-full hover:ring-primary/50 hover:ring-1 transition-all cursor-pointer">
          <div class="flex items-start gap-3">
            <UIcon :name="feature.icon" class="size-8 text-primary shrink-0 mt-0.5" />
            <div>
              <h3 class="font-semibold">{{ feature.title }}</h3>
              <p class="text-sm text-muted mt-1">{{ feature.description }}</p>
            </div>
          </div>
        </UCard>
      </NuxtLink>
    </div>
  </div>
</template>
