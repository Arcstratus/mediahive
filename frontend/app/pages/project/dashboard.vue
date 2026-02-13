<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const { getProjectCountByStatus, getUpcomingMilestones, getRecentProjects, findProjectById } = useDemoProjects()

const { counts, total } = getProjectCountByStatus()
const upcomingMilestones = getUpcomingMilestones()
const recentProjects = getRecentProjects(5)

function getMilestoneProjectName(projectId: number) {
  return findProjectById(projectId)?.name ?? ''
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: '專案總覽' },
    ]" />

    <h1 class="text-2xl font-bold">專案總覽</h1>

    <!-- 統計卡片 -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <UCard v-for="item in counts" :key="item.status">
        <div class="flex flex-col items-center gap-1">
          <span class="text-sm text-muted">{{ item.status }}</span>
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

    <!-- 近期里程碑 + 最近更新 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">近期里程碑</h3>
        </template>
        <div v-if="upcomingMilestones.length" class="flex flex-col gap-3">
          <div v-for="ms in upcomingMilestones" :key="ms.id" class="flex items-center justify-between">
            <div class="flex flex-col gap-0.5">
              <NuxtLink
                :to="`/project/${ms.projectId}/milestones/${ms.id}`"
                class="text-sm font-medium hover:text-primary transition-colors"
              >
                {{ ms.title }}
              </NuxtLink>
              <NuxtLink
                :to="`/project/${ms.projectId}`"
                class="text-xs text-muted hover:text-primary transition-colors"
              >
                {{ getMilestoneProjectName(ms.projectId) }}
              </NuxtLink>
            </div>
            <span class="text-xs text-muted shrink-0">{{ formatDate(ms.end_date) }}</span>
          </div>
        </div>
        <div v-else class="text-center text-muted py-4">
          無近期里程碑
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">最近更新的專案</h3>
        </template>
        <div v-if="recentProjects.length" class="flex flex-col gap-3">
          <NuxtLink
            v-for="p in recentProjects"
            :key="p.id"
            :to="`/project/${p.id}`"
            class="flex items-center justify-between hover:bg-elevated rounded-lg p-2 -mx-2 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium">{{ p.name }}</span>
              <UBadge
                :label="p.status"
                :color="(projectStatusColorMap[p.status] as any) ?? 'neutral'"
                variant="subtle"
                size="xs"
              />
            </div>
            <span class="text-xs text-muted shrink-0">{{ formatDate(p.updated_at) }}</span>
          </NuxtLink>
        </div>
        <div v-else class="text-center text-muted py-4">
          無專案資料
        </div>
      </UCard>
    </div>
  </div>
</template>
