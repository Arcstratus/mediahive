<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  name: '',
  email: '',
  phone: '',
  department: '',
  role: '',
  status: 'active' as 'active' | 'inactive',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立使用者
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '使用者已建立（Demo）', color: 'success' })
    navigateTo('/user')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '使用者管理', to: '/user' },
      { label: '新增使用者' },
    ]" />

    <UserFormLayout
      title="新增使用者"
      v-model:name="form.name"
      v-model:email="form.email"
      v-model:phone="form.phone"
      v-model:department="form.department"
      v-model:role="form.role"
      v-model:status="form.status"
      :loading="loading"
      @submit="onSubmit"
    />
  </div>
</template>
