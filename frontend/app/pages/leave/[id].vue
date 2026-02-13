<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

// TODO: 後端支援 - 從 API 取得請假資料
const items = [
  { id: 1, employee: '陳大文', type: '特休', start_date: '2025-02-10', end_date: '2025-02-12', reason: '家庭旅遊' },
  { id: 2, employee: '林小美', type: '病假', start_date: '2025-02-05', end_date: '2025-02-05', reason: '身體不適' },
  { id: 3, employee: '王志明', type: '事假', start_date: '2025-02-15', end_date: '2025-02-15', reason: '個人事務' },
  { id: 4, employee: '張雅婷', type: '公假', start_date: '2025-02-20', end_date: '2025-02-21', reason: '外部培訓課程' },
  { id: 5, employee: '李國華', type: '特休', start_date: '2025-03-01', end_date: '2025-03-07', reason: '出國旅遊' },
]

const id = Number(route.params.id)
const leave = items.find(item => item.id === id)

if (!leave) {
  throw createError({ statusCode: 404, statusMessage: '找不到此請假申請' })
}

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
  employee: leave.employee,
  type: leave.type,
  start_date: leave.start_date,
  end_date: leave.end_date,
  reason: leave.reason,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新請假申請
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '請假申請已更新（Demo）', color: 'success' })
    navigateTo('/leave')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '請假管理', to: '/leave' },
      { label: '編輯請假' },
    ]" />

    <h1 class="text-2xl font-bold">編輯請假</h1>

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
