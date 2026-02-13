<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const { getCustomerCountByLevel, getCustomerCountByIndustry, getRecentCustomers } = useDemoCustomers()

const { counts, total } = getCustomerCountByLevel()
const industryDistribution = getCustomerCountByIndustry()
const recentCustomers = getRecentCustomers(5)
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: '客戶總覽' },
    ]" />

    <h1 class="text-2xl font-bold">客戶總覽</h1>

    <!-- 統計卡片 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <UCard v-for="item in counts" :key="item.level">
        <div class="flex flex-col items-center gap-1">
          <span class="text-sm text-muted">{{ item.level }}</span>
          <span class="text-2xl font-bold">{{ item.count }}</span>
        </div>
      </UCard>
      <UCard>
        <div class="flex flex-col items-center gap-1">
          <span class="text-sm text-muted">合計</span>
          <span class="text-2xl font-bold">{{ total }}</span>
        </div>
      </UCard>
    </div>

    <!-- 產業分佈 + 最近更新 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">產業分佈</h3>
        </template>
        <div class="flex flex-col gap-3">
          <div v-for="item in industryDistribution" :key="item.industry" class="flex items-center justify-between">
            <span class="text-sm">{{ item.industry }}</span>
            <div class="flex items-center gap-2">
              <UProgress :value="item.count" :max="total" size="sm" class="w-32" />
              <span class="text-sm font-medium w-8 text-right">{{ item.count }}</span>
            </div>
          </div>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">最近更新的客戶</h3>
        </template>
        <div v-if="recentCustomers.length" class="flex flex-col gap-3">
          <NuxtLink
            v-for="c in recentCustomers"
            :key="c.id"
            :to="`/customer/${c.id}`"
            class="flex items-center justify-between hover:bg-elevated rounded-lg p-2 -mx-2 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium">{{ c.name }}</span>
              <UBadge
                :label="c.level"
                :color="(customerLevelColorMap[c.level] as any) ?? 'neutral'"
                variant="subtle"
                size="xs"
              />
            </div>
            <span class="text-xs text-muted shrink-0">{{ formatDate(c.updated_at) }}</span>
          </NuxtLink>
        </div>
        <div v-else class="text-center text-muted py-4">
          無客戶資料
        </div>
      </UCard>
    </div>
  </div>
</template>
