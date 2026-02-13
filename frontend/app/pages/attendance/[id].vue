<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得出勤資料
const demoItems = [
  { id: 1, employee: '陳大文', date: '2024-12-09', clock_in: '08:55', clock_out: '18:05', remark: '' },
  { id: 2, employee: '林小美', date: '2024-12-09', clock_in: '09:15', clock_out: '18:10', remark: '' },
  { id: 3, employee: '王志明', date: '2024-12-09', clock_in: '', clock_out: '', remark: '' },
  { id: 4, employee: '張雅婷', date: '2024-12-09', clock_in: '08:50', clock_out: '18:00', remark: '' },
  { id: 5, employee: '李國華', date: '2024-12-09', clock_in: '', clock_out: '', remark: '' },
]

const record = demoItems.find(item => item.id === id)

if (!record) {
  throw createError({ statusCode: 404, statusMessage: '找不到此紀錄' })
}

const employeeOptions = [
  { label: '陳大文', value: '陳大文' },
  { label: '林小美', value: '林小美' },
  { label: '王志明', value: '王志明' },
  { label: '張雅婷', value: '張雅婷' },
  { label: '李國華', value: '李國華' },
]

const form = reactive({
  employee: record.employee,
  date: record.date,
  clock_in: record.clock_in,
  clock_out: record.clock_out,
  remark: record.remark,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新出勤紀錄
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '出勤紀錄已更新（Demo）', color: 'success' })
    navigateTo('/attendance')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '出勤管理', to: '/attendance' },
      { label: '編輯紀錄' },
    ]" />

    <h1 class="text-2xl font-bold">編輯紀錄</h1>

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
