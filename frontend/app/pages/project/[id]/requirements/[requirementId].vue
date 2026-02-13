<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const projectId = Number(route.params.id)
const requirementId = Number(route.params.requirementId)

const { findProjectById, findRequirementById } = useDemoProjects()

const project = findProjectById(projectId)
if (!project) {
  throw createError({ statusCode: 404, statusMessage: '找不到該專案' })
}

const _req = findRequirementById(requirementId)
if (!_req || _req.projectId !== projectId) {
  throw createError({ statusCode: 404, statusMessage: '找不到該需求' })
}
const requirement = _req
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name, to: `/project/${projectId}` },
      { label: requirement.requirementNumber },
    ]" />

    <div class="flex items-center gap-3">
      <span class="text-muted">{{ requirement.requirementNumber }}</span>
      <h1 class="text-2xl font-bold">{{ requirement.title }}</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左側：描述與驗收標準 -->
      <div class="lg:col-span-2 flex flex-col gap-6">
        <UCard>
          <template #header>
            <h3 class="font-semibold">描述</h3>
          </template>
          <p class="text-sm whitespace-pre-wrap">{{ requirement.description }}</p>
        </UCard>

        <UCard v-if="requirement.acceptanceCriteria">
          <template #header>
            <h3 class="font-semibold">驗收標準</h3>
          </template>
          <p class="text-sm whitespace-pre-wrap">{{ requirement.acceptanceCriteria }}</p>
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
                  :label="requirement.status"
                  :color="(requirementStatusColorMap[requirement.status] as any) ?? 'neutral'"
                  variant="subtle"
                  size="sm"
                />
              </dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">優先級</dt>
              <dd>
                <UBadge
                  :label="requirement.priority"
                  :color="(requirementPriorityColorMap[requirement.priority] as any) ?? 'neutral'"
                  variant="subtle"
                  size="sm"
                />
              </dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">來源</dt>
              <dd>{{ requirement.source }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">建立時間</dt>
              <dd>{{ formatDate(requirement.created_at) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted">更新時間</dt>
              <dd>{{ formatDate(requirement.updated_at) }}</dd>
            </div>
          </dl>
        </UCard>
      </div>
    </div>
  </div>
</template>
