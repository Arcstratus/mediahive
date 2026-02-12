<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const { findByUuid } = useDemoUsers()

const uuid = route.params.uuid as string
const user = findByUuid(uuid)

if (!user) {
  throw createError({ statusCode: 404, statusMessage: '找不到此使用者' })
}

const form = reactive({
  name: user.name,
  email: user.email,
  phone: user.phone,
  department: user.department,
  role: user.role,
  status: user.status,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新使用者資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '使用者已更新（Demo）', color: 'success' })
    navigateTo('/foundation/user')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: 'Foundation', to: '/foundation' },
      { label: '使用者管理', to: '/foundation/user' },
      { label: '編輯使用者' },
    ]" />

    <UserFormLayout
      title="編輯使用者"
      :avatar="user.avatar"
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
