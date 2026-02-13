<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()
const { departments } = useDemoDepartments()

const parentOptions = computed(() => [
  { label: '（無上級部門）', value: 0 },
  ...departments.value.map(d => ({ label: d.name, value: d.id })),
])

const form = reactive({
  name: '',
  parentId: 0,
  head: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立部門
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '部門已建立（Demo）', color: 'success' })
    navigateTo('/foundation/department')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: 'Foundation', to: '/foundation' },
      { label: '組織架構', to: '/foundation/department' },
      { label: '新增部門' },
    ]" />

    <h1 class="text-2xl font-bold">新增部門</h1>

    <div class="max-w-xl">
      <UCard>
        <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
          <UFormField label="部門名稱">
            <UInput v-model="form.name" placeholder="請輸入部門名稱" icon="i-lucide-building" />
          </UFormField>

          <UFormField label="上級部門">
            <USelectMenu v-model="form.parentId" :items="parentOptions" value-key="value" placeholder="請選擇上級部門" />
          </UFormField>

          <UFormField label="部門主管">
            <UInput v-model="form.head" placeholder="請輸入主管姓名" icon="i-lucide-user" />
          </UFormField>

          <div class="flex justify-end gap-2 pt-4">
            <UButton label="取消" variant="outline" color="neutral" to="/foundation/department" />
            <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
