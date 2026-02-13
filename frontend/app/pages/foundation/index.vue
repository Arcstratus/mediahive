<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
})

const features = [
  { title: '使用者管理', description: '建立與管理使用者帳號、角色與權限', icon: 'i-lucide-users', to: '/foundation/user' },
  { title: '組織架構', description: '定義公司部門、團隊與層級結構', icon: 'i-lucide-building', to: '/foundation/department' },
  { title: '角色權限', description: '管理系統角色與存取權限設定', icon: 'i-lucide-shield', to: '/foundation/role' },
  { title: '系統設定', description: '管理系統參數、環境設定與全域偏好設定', icon: 'i-lucide-settings', to: '/foundation/settings' },
  { title: '通知中心', description: '管理系統通知、郵件範本與推播設定', icon: 'i-lucide-bell', to: '/foundation/notification' },
  { title: '稽核日誌', description: '追蹤系統操作紀錄與變更歷史', icon: 'i-lucide-scroll-text', to: '/foundation/audit-log' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'Foundation' }]" />

    <h1 class="text-2xl font-bold">Foundation 基礎模組</h1>
    <p class="text-muted">系統核心基礎功能，包含設定、使用者管理與組織架構。</p>

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
