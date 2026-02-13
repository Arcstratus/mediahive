<script setup lang="ts">
import { allDomains } from '~/services/domains'

definePageMeta({
  layout: 'dashboard',
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">Mediahive</h1>
    <p class="text-muted">選擇服務開始使用。</p>

    <div v-for="domain in allDomains" :key="domain.id" class="flex flex-col gap-4">
      <div class="flex items-center gap-2">
        <UIcon :name="domain.icon" class="size-5 text-primary" />
        <h2 class="text-lg font-semibold">{{ domain.label }}</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <NuxtLink v-for="service in domain.services" :key="service.id" :to="service.path">
          <UCard class="h-full hover:ring-primary/50 hover:ring-1 transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <UIcon :name="service.icon" class="size-6 text-primary shrink-0" />
              <span class="font-medium">{{ service.label }}</span>
            </div>
          </UCard>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
