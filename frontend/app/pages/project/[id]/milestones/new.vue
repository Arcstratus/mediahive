<script setup lang="ts">
import type { MilestoneStatus } from '~/types'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const projectId = Number(route.params.id)

const { findProjectById, getProjectRequirements } = useDemoProjects()

const project = findProjectById(projectId)
if (!project) {
  throw createError({ statusCode: 404, statusMessage: '找不到該專案' })
}

const projectRequirements = getProjectRequirements(projectId)
const statusOptions: MilestoneStatus[] = ['未開始', '進行中', '已完成', '已逾期']

const requirementOptions = projectRequirements.map(r => ({
  label: `${r.requirementNumber} ${r.title}`,
  value: r.id,
}))

const form = reactive({
  title: '',
  description: '',
  status: '未開始' as MilestoneStatus,
  start_date: '',
  end_date: '',
  requirementIds: [] as number[],
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立里程碑
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '里程碑已建立（Demo）', color: 'success' })
    navigateTo(`/project/${projectId}`)
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name, to: `/project/${projectId}` },
      { label: '新增里程碑' },
    ]" />

    <h1 class="text-2xl font-bold">新增里程碑</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="標題" required>
          <UInput v-model="form.title" placeholder="輸入里程碑標題" class="w-full" />
        </UFormField>

        <UFormField label="描述">
          <UTextarea v-model="form.description" placeholder="輸入里程碑描述" class="w-full" :rows="4" />
        </UFormField>

        <UFormField label="狀態">
          <USelectMenu v-model="form.status" :items="statusOptions" class="w-full" />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="開始日期">
            <UInput v-model="form.start_date" type="date" class="w-full" />
          </UFormField>

          <UFormField label="結束日期">
            <UInput v-model="form.end_date" type="date" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="對應需求">
          <USelectMenu
            v-model="form.requirementIds"
            :items="requirementOptions"
            multiple
            placeholder="選擇對應需求"
            value-key="value"
            class="w-full"
          />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" :to="`/project/${projectId}`" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
