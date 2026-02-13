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

const form = reactive({
  position: '',
  department: '',
  description: '',
  headcount: 1,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立職缺
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '職缺已建立（Demo）', color: 'success' })
    navigateTo('/recruitment')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '招募管理', to: '/recruitment' },
      { label: '新增職缺' },
    ]" />

    <h1 class="text-2xl font-bold">新增職缺</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="職缺名稱" required>
            <UInput v-model="form.position" placeholder="請輸入職缺名稱" icon="i-lucide-briefcase" />
          </UFormField>

          <UFormField label="部門">
            <USelectMenu v-model="form.department" :items="departmentOptions" value-key="value" placeholder="請選擇部門" />
          </UFormField>

          <UFormField label="工作說明">
            <UTextarea v-model="form.description" placeholder="請輸入工作說明" />
          </UFormField>

          <UFormField label="需求人數">
            <UInput v-model="form.headcount" type="number" placeholder="請輸入需求人數" icon="i-lucide-users" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/recruitment" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
