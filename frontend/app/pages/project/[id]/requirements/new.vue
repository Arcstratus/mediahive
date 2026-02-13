<script setup lang="ts">
import type { RequirementStatus, RequirementPriority } from '~/types'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const projectId = Number(route.params.id)

const { findProjectById } = useDemoProjects()
const project = findProjectById(projectId)
if (!project) {
  throw createError({ statusCode: 404, statusMessage: '找不到該專案' })
}

const statusOptions: RequirementStatus[] = ['草稿', '已確認', '開發中', '已交付', '已取消']
const priorityOptions: RequirementPriority[] = ['必要', '重要', '一般', '可選']

const form = reactive({
  requirementNumber: '',
  title: '',
  description: '',
  status: '草稿' as RequirementStatus,
  priority: '一般' as RequirementPriority,
  source: '',
  acceptanceCriteria: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立需求
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '需求已建立（Demo）', color: 'success' })
    navigateTo(`/project/${projectId}`)
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name, to: `/project/${projectId}` },
      { label: '新增需求' },
    ]" />

    <h1 class="text-2xl font-bold">新增客戶需求</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="需求編號" required>
            <UInput v-model="form.requirementNumber" placeholder="例：REQ-007" class="w-full" />
          </UFormField>

          <UFormField label="優先級">
            <USelectMenu v-model="form.priority" :items="priorityOptions" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="標題" required>
          <UInput v-model="form.title" placeholder="輸入需求標題" class="w-full" />
        </UFormField>

        <UFormField label="描述">
          <UTextarea v-model="form.description" placeholder="輸入需求描述" class="w-full" :rows="4" />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="狀態">
            <USelectMenu v-model="form.status" :items="statusOptions" class="w-full" />
          </UFormField>

          <UFormField label="來源">
            <UInput v-model="form.source" placeholder="例：倉管部" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="驗收標準">
          <UTextarea v-model="form.acceptanceCriteria" placeholder="輸入驗收標準（每行一條）" class="w-full" :rows="4" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" :to="`/project/${projectId}`" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
