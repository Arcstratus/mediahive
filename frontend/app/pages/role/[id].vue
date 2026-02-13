<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const { findById } = useDemoRoles()

const id = Number(route.params.id)
const role = findById(id)

if (!role) {
  throw createError({ statusCode: 404, statusMessage: '找不到此角色' })
}

// TODO: 後端支援 - 從 API 取得可用權限列表
const allPermissions = [
  '系統設定', '使用者管理', '角色管理', '部門管理',
  '稽核日誌', '通知管理', '使用者檢視', '報表檢視',
  '個人資料', '資源檢視', '資源管理', '書籤管理',
]

const form = reactive({
  name: role.name,
  description: role.description,
  permissions: [...role.permissions],
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新角色
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '角色已更新（Demo）', color: 'success' })
    navigateTo('/role')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '角色權限', to: '/role' },
      { label: '編輯角色' },
    ]" />

    <h1 class="text-2xl font-bold">編輯角色</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="角色名稱">
            <UInput v-model="form.name" placeholder="請輸入角色名稱" icon="i-lucide-shield" />
          </UFormField>

          <UFormField label="說明">
            <UTextarea v-model="form.description" placeholder="請輸入角色說明" />
          </UFormField>

          <UFormField label="權限">
            <div class="flex flex-wrap gap-2">
              <UCheckbox
                v-for="perm in allPermissions"
                :key="perm"
                :label="perm"
                :model-value="form.permissions.includes(perm)"
                @update:model-value="(val: boolean) => {
                  if (val) form.permissions.push(perm)
                  else form.permissions = form.permissions.filter(p => p !== perm)
                }"
              />
            </div>
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/role" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
