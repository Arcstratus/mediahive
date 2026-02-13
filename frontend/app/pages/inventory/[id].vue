<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

// TODO: 後端支援 - 從 API 取得品項資料
const demoItems = [
  { id: 1, name: '筆記型電腦', spec: '14 吋 / 16GB / 512GB SSD', quantity: 45, warehouse: 'A 倉' },
  { id: 2, name: '印表機碳粉', spec: '黑色 / 相容型號 HP-26A', quantity: 8, warehouse: 'B 倉' },
  { id: 3, name: 'A4 影印紙', spec: '80 磅 / 每箱 5 包', quantity: 120, warehouse: 'A 倉' },
  { id: 4, name: '螢幕', spec: '27 吋 4K IPS', quantity: 22, warehouse: 'A 倉' },
  { id: 5, name: '鍵盤滑鼠組', spec: '無線 / 中文注音', quantity: 3, warehouse: 'B 倉' },
]

const id = Number(route.params.id)
const item = demoItems.find(i => i.id === id)

if (!item) {
  throw createError({ statusCode: 404, statusMessage: '找不到此品項' })
}

const form = reactive({
  name: item.name,
  spec: item.spec,
  quantity: item.quantity,
  warehouse: item.warehouse,
})

const warehouseOptions = ['A 倉', 'B 倉', 'C 倉']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新品項資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '品項已更新（Demo）', color: 'success' })
    navigateTo('/inventory')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '庫存管理', to: '/inventory' },
      { label: '編輯品項' },
    ]" />

    <h1 class="text-2xl font-bold">編輯品項</h1>

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
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
