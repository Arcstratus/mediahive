<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const { findById } = useDemoEmployees()

const id = Number(route.params.id)
const employee = findById(id)

if (!employee) {
  throw createError({ statusCode: 404, statusMessage: '找不到此員工' })
}

const departmentOptions = [
  { label: '資訊部', value: '資訊部' },
  { label: '人資部', value: '人資部' },
  { label: '業務部', value: '業務部' },
  { label: '財務部', value: '財務部' },
  { label: '研發部', value: '研發部' },
]

const statusOptions = [
  { label: '啟用', value: 'active' },
  { label: '停用', value: 'inactive' },
]

const form = reactive({
  name: employee.name,
  email: employee.email,
  phone: employee.phone,
  department: employee.department,
  position: employee.position,
  status: employee.status,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新員工資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '員工已更新（Demo）', color: 'success' })
    navigateTo('/hrm/employee')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: 'HRM', to: '/hrm' },
      { label: '員工管理', to: '/hrm/employee' },
      { label: '編輯員工' },
    ]" />

    <h1 class="text-2xl font-bold">編輯員工</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="姓名">
            <UInput v-model="form.name" placeholder="請輸入姓名" icon="i-lucide-user" />
          </UFormField>

          <UFormField label="電子郵件">
            <UInput v-model="form.email" type="email" placeholder="請輸入電子郵件" icon="i-lucide-mail" />
          </UFormField>

          <UFormField label="電話">
            <UInput v-model="form.phone" placeholder="請輸入電話號碼" icon="i-lucide-phone" />
          </UFormField>

          <UFormField label="部門">
            <USelectMenu v-model="form.department" :items="departmentOptions" value-key="value" placeholder="請選擇部門" />
          </UFormField>

          <UFormField label="職位">
            <UInput v-model="form.position" placeholder="請輸入職位" icon="i-lucide-briefcase" />
          </UFormField>

          <UFormField label="狀態">
            <USelectMenu v-model="form.status" :items="statusOptions" value-key="value" placeholder="請選擇狀態" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/hrm/employee" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
