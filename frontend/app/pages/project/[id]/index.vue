<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const id = Number(route.params.id)

const { findProjectById, getProjectMilestones, getProjectRequirements, getMilestonesByStatus, findRequirementById } = useDemoProjects()

const project = findProjectById(id)
if (!project) {
  throw createError({ statusCode: 404, statusMessage: '找不到該專案' })
}

const milestones = computed(() => getProjectMilestones(id))
const requirements = getProjectRequirements(id)

// 里程碑列表/看板切換
const milestoneView = useState(`project-${id}-milestone-view`, () => 'list')
const milestoneViewTabs = [
  { label: '列表', value: 'list' },
  { label: '看板', value: 'kanban' },
]

const milestoneKanbanColumns = computed(() => getMilestonesByStatus(id))

// 取得里程碑對應的需求名稱
function getRequirementTitles(requirementIds: number[]) {
  return requirementIds
    .map(rid => findRequirementById(rid))
    .filter(r => r !== null)
    .map(r => r.title)
}

// 結案
const showCloseConfirm = ref(false)

function onCloseProject() {
  showCloseConfirm.value = true
}

function confirmCloseProject() {
  project.status = '已結案'
  showCloseConfirm.value = false
  toast.add({ title: '專案已結案（Demo）', color: 'success' })
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name },
    ]" />

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <h1 class="text-2xl font-bold">{{ project.name }}</h1>
        <UBadge
          :label="project.status"
          :color="(projectStatusColorMap[project.status] as any) ?? 'neutral'"
          variant="subtle"
        />
      </div>
      <div class="flex items-center gap-2">
        <UButton
          v-if="project.status !== '已結案'"
          label="編輯"
          icon="i-lucide-pencil"
          variant="outline"
          :to="`/project/${id}/edit`"
        />
        <UButton
          v-if="project.status !== '已結案'"
          label="結案"
          icon="i-lucide-check-circle"
          color="success"
          variant="outline"
          @click="onCloseProject"
        />
      </div>
    </div>

    <!-- ① 專案資訊 + 進度 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">專案資訊</h3>
        </template>
        <dl class="flex flex-col gap-3">
          <div class="flex justify-between">
            <dt class="text-muted">專案編號</dt>
            <dd>{{ project.code }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">客戶</dt>
            <dd>{{ project.customer }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">專案經理</dt>
            <dd>{{ project.manager }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">團隊成員</dt>
            <dd>{{ project.members.join('、') }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">時程</dt>
            <dd>{{ formatDate(project.start_date) }} ~ {{ formatDate(project.end_date) }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">預算</dt>
            <dd>NT$ {{ project.budget.toLocaleString() }}</dd>
          </div>
        </dl>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">進度</h3>
        </template>
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-4">
            <UProgress :value="project.progress" size="lg" class="flex-1" />
            <span class="text-lg font-bold">{{ project.progress }}%</span>
          </div>
          <p class="text-sm text-muted">{{ project.description }}</p>
        </div>
      </UCard>
    </div>

    <!-- ② 客戶需求 -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">客戶需求</h3>
          <UButton label="新增需求" icon="i-lucide-plus" size="sm" variant="outline" :to="`/project/${id}/requirements/new`" />
        </div>
      </template>
      <div v-if="requirements.length" class="flex flex-col gap-3">
        <NuxtLink
          v-for="req in requirements"
          :key="req.id"
          :to="`/project/${id}/requirements/${req.id}`"
          class="flex items-center justify-between p-3 rounded-lg hover:bg-elevated transition-colors"
        >
          <div class="flex items-center gap-3">
            <span class="text-xs text-muted">{{ req.requirementNumber }}</span>
            <span class="text-sm font-medium">{{ req.title }}</span>
            <UBadge
              :label="req.priority"
              :color="(requirementPriorityColorMap[req.priority] as any) ?? 'neutral'"
              variant="subtle"
              size="xs"
            />
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
        尚無客戶需求
      </div>
    </UCard>

    <!-- ③ 交付規劃（里程碑） -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">交付規劃</h3>
          <UButton label="新增里程碑" icon="i-lucide-plus" size="sm" variant="outline" :to="`/project/${id}/milestones/new`" />
        </div>
      </template>

      <div class="flex flex-col gap-4">
        <UTabs v-model="milestoneView" :items="milestoneViewTabs" />

        <!-- 列表 View -->
        <div v-if="milestoneView === 'list'" class="flex flex-col gap-4">
          <NuxtLink
            v-for="ms in milestones"
            :key="ms.id"
            :to="`/project/${id}/milestones/${ms.id}`"
            class="block"
          >
            <UCard class="hover:ring-1 hover:ring-primary transition-all cursor-pointer">
              <div class="flex flex-col gap-2">
                <div class="flex items-center justify-between">
                  <span class="font-medium">{{ ms.title }}</span>
                  <UBadge
                    :label="ms.status"
                    :color="(milestoneStatusColorMap[ms.status] as any) ?? 'neutral'"
                    variant="subtle"
                    size="sm"
                  />
                </div>
                <span class="text-xs text-muted">{{ formatDate(ms.start_date) }} ~ {{ formatDate(ms.end_date) }}</span>
                <UProgress :value="ms.progress" size="sm" />
                <p v-if="ms.requirementIds.length" class="text-xs text-muted">
                  對應需求：{{ getRequirementTitles(ms.requirementIds).join('、') }}
                </p>
              </div>
            </UCard>
          </NuxtLink>
          <div v-if="!milestones.length" class="text-center text-muted py-4">
            尚無里程碑
          </div>
        </div>

        <!-- 看板 View -->
        <div v-if="milestoneView === 'kanban'" class="flex gap-4 overflow-x-auto pb-4">
          <div
            v-for="col in milestoneKanbanColumns"
            :key="col.status"
            class="w-64 flex-shrink-0 flex flex-col gap-3"
          >
            <div class="flex items-center gap-2 px-1">
              <UBadge
                :label="col.status"
                :color="(milestoneStatusColorMap[col.status] as any) ?? 'neutral'"
                variant="subtle"
                size="sm"
              />
              <span class="text-xs text-muted">({{ col.milestones.length }})</span>
            </div>

            <div class="flex flex-col gap-2 min-h-24 rounded-lg bg-elevated p-2">
              <NuxtLink
                v-for="ms in col.milestones"
                :key="ms.id"
                :to="`/project/${id}/milestones/${ms.id}`"
                class="block"
              >
                <UCard class="hover:ring-1 hover:ring-primary transition-all cursor-pointer">
                  <div class="flex flex-col gap-1">
                    <span class="text-sm font-medium">{{ ms.title }}</span>
                    <span class="text-xs text-muted">{{ formatDate(ms.start_date) }} ~ {{ formatDate(ms.end_date) }}</span>
                    <div class="flex items-center gap-2">
                      <UProgress :value="ms.progress" size="xs" class="flex-1" />
                      <span class="text-xs text-muted">{{ ms.progress }}%</span>
                    </div>
                  </div>
                </UCard>
              </NuxtLink>

              <div v-if="!col.milestones.length" class="flex items-center justify-center h-16 text-xs text-muted">
                無里程碑
              </div>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- ④ 結案 -->
    <UCard>
      <template #header>
        <h3 class="font-semibold">結案</h3>
      </template>
      <div v-if="project.status === '已結案'" class="text-sm text-muted">
        已於 {{ formatDate(project.updated_at) }} 結案
      </div>
      <div v-else class="flex flex-col gap-2">
        <p class="text-sm text-muted">確認所有交付項目完成後，可將專案結案。未來將觸發 BPM 開立驗收/請款單。</p>
        <div>
          <UButton
            label="結案"
            icon="i-lucide-check-circle"
            color="success"
            @click="onCloseProject"
          />
        </div>
      </div>
    </UCard>

    <!-- 結案確認對話框 -->
    <UModal v-model:open="showCloseConfirm">
      <template #content>
        <UCard>
          <template #header>
            <h3 class="font-semibold">確認結案</h3>
          </template>
          <p class="text-sm">確定要將「{{ project.name }}」結案嗎？結案後將無法再編輯。</p>
          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton label="取消" color="neutral" variant="outline" @click="showCloseConfirm = false" />
              <UButton label="確認結案" color="success" @click="confirmCloseProject" />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
