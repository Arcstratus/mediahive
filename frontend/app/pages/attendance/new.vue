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

const form = reactive({
  employee: '',
  date: '',
  clock_in: '',
  clock_out: '',
  remark: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立出勤紀錄
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '出勤紀錄已建立（Demo）', color: 'success' })
    navigateTo('/attendance')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '出勤管理', to: '/attendance' },
      { label: '新增紀錄' },
    ]" />

    <h1 class="text-2xl font-bold">新增紀錄</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="員工" required>
            <USelectMenu v-model="form.employee" :items="employeeOptions" value-key="value" placeholder="請選擇員工" />
          </UFormField>

          <UFormField label="日期">
            <UInput v-model="form.date" type="date" />
          </UFormField>

          <UFormField label="上班打卡">
            <UInput v-model="form.clock_in" type="time" />
          </UFormField>

          <UFormField label="下班打卡">
            <UInput v-model="form.clock_out" type="time" />
          </UFormField>

          <UFormField label="備註">
            <UTextarea v-model="form.remark" placeholder="請輸入備註" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/attendance" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
