<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
})

const features = [
  { title: '庫存管理', description: '追蹤商品庫存數量、位置與批號', icon: 'i-lucide-warehouse', to: '/erp/inventory' },
  { title: '採購管理', description: '管理供應商、採購單與進貨流程', icon: 'i-lucide-shopping-cart', to: '/erp/purchase' },
  { title: '銷售管理', description: '處理訂單、報價單與出貨作業', icon: 'i-lucide-receipt', to: '/erp/sales' },
  { title: '財務會計', description: '管理帳務、發票與財務報表', icon: 'i-lucide-calculator', to: '/erp/finance' },
  { title: '生產製造', description: '規劃生產排程、BOM 與工單管理', icon: 'i-lucide-factory', to: '/erp/production' },
  { title: '物流配送', description: '管理出貨排程、運送追蹤與配送路線', icon: 'i-lucide-truck', to: '/erp/logistics' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: 'ERP' }]" />

    <h1 class="text-2xl font-bold">ERP 企業資源規劃</h1>
    <p class="text-muted">整合庫存、採購、銷售與財務等企業核心流程。</p>

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
