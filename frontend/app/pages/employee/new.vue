<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

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
  name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  status: 'active' as 'active' | 'inactive',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立員工
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '員工已建立（Demo）', color: 'success' })
    navigateTo('/employee')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '員工管理', to: '/employee' },
      { label: '新增員工' },
    ]" />

    <h1 class="text-2xl font-bold">新增員工</h1>

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
            <UButton label="取消" variant="outline" color="neutral" to="/employee" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
