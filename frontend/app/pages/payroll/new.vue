<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const employeeOptions = ['陳大文', '林小美', '王志明', '張雅婷', '李國華']

const form = reactive({
  employee: '',
  month: '',
  base_salary: '',
  overtime_pay: '',
  deductions: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立薪資單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '薪資單已建立（Demo）', color: 'success' })
    navigateTo('/payroll')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '薪資管理', to: '/payroll' },
      { label: '新增薪資單' },
    ]" />

    <h1 class="text-2xl font-bold">新增薪資單</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="員工" required>
          <USelectMenu v-model="form.employee" :items="employeeOptions" placeholder="選擇員工" class="w-full" />
        </UFormField>

        <UFormField label="月份">
          <UInput v-model="form.month" type="month" class="w-full" />
        </UFormField>

        <UFormField label="基本薪資">
          <UInput v-model="form.base_salary" type="number" placeholder="輸入基本薪資" class="w-full" />
        </UFormField>

        <UFormField label="加班費">
          <UInput v-model="form.overtime_pay" type="number" placeholder="輸入加班費" class="w-full" />
        </UFormField>

        <UFormField label="扣項">
          <UInput v-model="form.deductions" type="number" placeholder="輸入扣項" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/payroll" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
