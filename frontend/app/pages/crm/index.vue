<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
})

const features = [
  { title: '客戶管理', description: '維護客戶資料、聯絡人與互動紀錄', icon: 'i-lucide-contact' },
  { title: '商機管理', description: '追蹤銷售機會、階段進度與成交預測', icon: 'i-lucide-target' },
  { title: '合約管理', description: '管理合約簽訂、續約與到期提醒', icon: 'i-lucide-file-signature' },
  { title: '行銷活動', description: '規劃行銷活動、追蹤成效與轉換率', icon: 'i-lucide-megaphone' },
  { title: '客服工單', description: '處理客訴、服務請求與滿意度調查', icon: 'i-lucide-headset' },
  { title: '報表分析', description: '檢視銷售儀表板、趨勢分析與客戶分群', icon: 'i-lucide-chart-bar' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'CRM' }]" />

    <h1 class="text-2xl font-bold">CRM 客戶關係管理</h1>
    <p class="text-muted">管理客戶、商機、合約與行銷活動等客戶關係。</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard v-for="feature in features" :key="feature.title">
        <div class="flex items-start gap-3">
          <UIcon :name="feature.icon" class="size-8 text-primary shrink-0 mt-0.5" />
          <div>
            <h3 class="font-semibold">{{ feature.title }}</h3>
            <p class="text-sm text-muted mt-1">{{ feature.description }}</p>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>
