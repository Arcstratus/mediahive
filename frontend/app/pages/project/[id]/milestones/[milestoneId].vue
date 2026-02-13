<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const projectId = Number(route.params.id)
const milestoneId = Number(route.params.milestoneId)

const { findProjectById, findMilestoneById, getMilestoneRequirements } = useDemoProjects()

const project = findProjectById(projectId)
if (!project) {
  throw createError({ statusCode: 404, statusMessage: '找不到該專案' })
}

const _ms = findMilestoneById(milestoneId)
if (!_ms || _ms.projectId !== projectId) {
  throw createError({ statusCode: 404, statusMessage: '找不到該里程碑' })
}
const milestone = _ms

const milestoneRequirements = getMilestoneRequirements(milestoneId)
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name, to: `/project/${projectId}` },
      { label: milestone.title },
    ]" />

    <div class="flex items-center gap-3">
      <h1 class="text-2xl font-bold">{{ milestone.title }}</h1>
      <UBadge
        :label="milestone.status"
        :color="(milestoneStatusColorMap[milestone.status] as any) ?? 'neutral'"
        variant="subtle"
      />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左側：描述與對應需求 -->
      <div class="lg:col-span-2 flex flex-col gap-6">
        <UCard>
          <template #header>
            <h3 class="font-semibold">描述</h3>
          </template>
          <p class="text-sm whitespace-pre-wrap">{{ milestone.description }}</p>
        </UCard>

        <UCard>
          <template #header>
            <h3 class="font-semibold">對應需求</h3>
          </template>
          <div v-if="milestoneRequirements.length" class="flex flex-col gap-3">
            <NuxtLink
              v-for="req in milestoneRequirements"
              :key="req.id"
              :to="`/project/${projectId}/requirements/${req.id}`"
              class="flex items-center justify-between p-3 rounded-lg hover:bg-elevated transition-colors"
            >
              <div class="flex items-center gap-3">
                <span class="text-xs text-muted">{{ req.requirementNumber }}</span>
                <span class="text-sm font-medium">{{ req.title }}</span>
              </div>
              <UBadge
                :label="req.status"
                :color="(requirementStatusColorMap[req.status] as any) ?? 'neutral'"
                variant="subtle"
                size="sm"
              />
            </NuxtLink>
          </div>
          <div v-else class="text-center text-muted py-4">
            無對應需求
          </div>
        </UCard>
      </div>

      <!-- 右側：屬性 -->
      <div>
        <UCard>
          <template #header>
            <h3 class="font-semibold">屬性</h3>
          </template>
          <dl class="flex flex-col gap-3">
            <div class="flex justify-between">
              <dt class="text-muted">狀態</dt>
              <dd>
                <UBadge
                  :label="milestone.status"
                  :color="(milestoneStatusColorMap[milestone.status] as any) ?? 'neutral'"
                  variant="subtle"
                  size="sm"
                />
              </dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">時程</dt>
              <dd>{{ formatDate(milestone.start_date) }} ~ {{ formatDate(milestone.end_date) }}</dd>
            </div>
            <div class="flex flex-col gap-1">
              <dt class="text-muted">進度</dt>
              <dd>
                <div class="flex items-center gap-2">
                  <UProgress :value="milestone.progress" size="sm" class="flex-1" />
                  <span class="text-sm">{{ milestone.progress }}%</span>
                </div>
              </dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">建立時間</dt>
              <dd>{{ formatDate(milestone.created_at) }}</dd>
            </div>
          </dl>
        </UCard>
      </div>
    </div>
  </div>
</template>
