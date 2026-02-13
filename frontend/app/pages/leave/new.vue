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

const typeOptions = [
  { label: '特休', value: '特休' },
  { label: '病假', value: '病假' },
  { label: '事假', value: '事假' },
  { label: '公假', value: '公假' },
  { label: '婚假', value: '婚假' },
]

const form = reactive({
  employee: '',
  type: '',
  start_date: '',
  end_date: '',
  reason: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立請假申請
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '請假申請已建立（Demo）', color: 'success' })
    navigateTo('/leave')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '請假管理', to: '/leave' },
      { label: '新增請假' },
    ]" />

    <h1 class="text-2xl font-bold">新增請假</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="員工" required>
            <USelectMenu v-model="form.employee" :items="employeeOptions" value-key="value" placeholder="請選擇員工" />
          </UFormField>

          <UFormField label="假別">
            <USelectMenu v-model="form.type" :items="typeOptions" value-key="value" placeholder="請選擇假別" />
          </UFormField>

          <UFormField label="開始日期">
            <UInput v-model="form.start_date" type="date" />
          </UFormField>

          <UFormField label="結束日期">
            <UInput v-model="form.end_date" type="date" />
          </UFormField>

          <UFormField label="事由" required>
            <UTextarea v-model="form.reason" placeholder="請輸入請假事由" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/leave" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
