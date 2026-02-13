<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const employeeOptions = [
  { label: '陳大文', value: '陳大文' },
  { label: '林小美', value: '林小美' },
  { label: '王志明', value: '王志明' },
  { label: '張雅婷', value: '張雅婷' },
  { label: '李國華', value: '李國華' },
]

const periodOptions = [
  { label: '2024 H1', value: '2024 H1' },
  { label: '2024 H2', value: '2024 H2' },
  { label: '2025 H1', value: '2025 H1' },
  { label: '2025 H2', value: '2025 H2' },
]

const gradeOptions = [
  { label: 'A', value: 'A' },
  { label: 'B', value: 'B' },
  { label: 'C', value: 'C' },
  { label: 'D', value: 'D' },
]

const form = reactive({
  employee: '',
  period: '',
  kpi_rate: '',
  grade: '',
  comment: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立績效考核
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '考核已建立（Demo）', color: 'success' })
    navigateTo('/performance')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '績效考核', to: '/performance' },
      { label: '新增考核' },
    ]" />

    <h1 class="text-2xl font-bold">新增考核</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="員工" required>
            <USelectMenu v-model="form.employee" :items="employeeOptions" value-key="value" placeholder="請選擇員工" />
          </UFormField>

          <UFormField label="考核期間">
            <USelectMenu v-model="form.period" :items="periodOptions" value-key="value" placeholder="請選擇考核期間" />
          </UFormField>

          <UFormField label="KPI 達成率">
            <UInput v-model="form.kpi_rate" placeholder="例如 95%" />
          </UFormField>

          <UFormField label="評等">
            <USelectMenu v-model="form.grade" :items="gradeOptions" value-key="value" placeholder="請選擇評等" />
          </UFormField>

          <UFormField label="主管評語">
            <UTextarea v-model="form.comment" placeholder="請輸入主管評語" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/performance" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
