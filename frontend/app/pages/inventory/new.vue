<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  name: '',
  spec: '',
  quantity: 0,
  warehouse: '',
})

const warehouseOptions = ['A 倉', 'B 倉', 'C 倉']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立品項
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '品項已建立（Demo）', color: 'success' })
    navigateTo('/inventory')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '庫存管理', to: '/inventory' },
      { label: '新增品項' },
    ]" />

    <h1 class="text-2xl font-bold">新增品項</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="品名" required>
          <UInput v-model="form.name" placeholder="輸入品名" class="w-full" />
        </UFormField>

        <UFormField label="規格">
          <UInput v-model="form.spec" placeholder="輸入規格" class="w-full" />
        </UFormField>

        <UFormField label="數量">
          <UInput v-model="form.quantity" type="number" placeholder="輸入數量" class="w-full" />
        </UFormField>

        <UFormField label="倉庫">
          <USelectMenu v-model="form.warehouse" :items="warehouseOptions" placeholder="選擇倉庫" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/inventory" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
