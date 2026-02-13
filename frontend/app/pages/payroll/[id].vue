<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得薪資資料
const demoData = [
  { id: 1, employee: '陳大文', month: '2024-11', base_salary: 55000, overtime_pay: 3200, deductions: 5800 },
  { id: 2, employee: '林小美', month: '2024-11', base_salary: 48000, overtime_pay: 1500, deductions: 4950 },
  { id: 3, employee: '王志明', month: '2024-11', base_salary: 65000, overtime_pay: 0, deductions: 7200 },
  { id: 4, employee: '張雅婷', month: '2024-11', base_salary: 52000, overtime_pay: 2400, deductions: 5440 },
  { id: 5, employee: '李國華', month: '2024-11', base_salary: 72000, overtime_pay: 4800, deductions: 8680 },
]

const item = demoData.find(d => d.id === id)

if (!item) {
  throw createError({ statusCode: 404, statusMessage: '找不到此薪資單' })
}

const employeeOptions = ['陳大文', '林小美', '王志明', '張雅婷', '李國華']

const form = reactive({
  employee: item.employee,
  month: item.month,
  base_salary: item.base_salary,
  overtime_pay: item.overtime_pay,
  deductions: item.deductions,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新薪資單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '薪資單已更新（Demo）', color: 'success' })
    navigateTo('/payroll')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '薪資管理', to: '/payroll' },
      { label: '編輯薪資單' },
    ]" />

    <h1 class="text-2xl font-bold">編輯薪資單</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="員工" required>
          <USelectMenu v-model="form.employee" :items="employeeOptions" placeholder="選擇員工" class="w-full" />
        </UFormField>

        <UFormField label="月份">
          <UInput v-model="form.month" type="month" class="w-full" />
        </UFormField>

        <UFormField label="基本薪資">
          <UInput v-model.number="form.base_salary" type="number" placeholder="輸入基本薪資" class="w-full" />
        </UFormField>

        <UFormField label="加班費">
          <UInput v-model.number="form.overtime_pay" type="number" placeholder="輸入加班費" class="w-full" />
        </UFormField>

        <UFormField label="扣項">
          <UInput v-model.number="form.deductions" type="number" placeholder="輸入扣項" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/payroll" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
