<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得採購單資料
const demoData = [
  { id: 1, orderNo: 'PO-20250101', supplier: '大同資訊股份有限公司', itemCount: 5, amount: 152000, note: '年度設備採購' },
  { id: 2, orderNo: 'PO-20250102', supplier: '聯強國際', itemCount: 3, amount: 87500, note: '網路設備更新' },
  { id: 3, orderNo: 'PO-20250103', supplier: '全國電子', itemCount: 8, amount: 234000, note: '辦公室設備' },
  { id: 4, orderNo: 'PO-20250104', supplier: '震旦行', itemCount: 2, amount: 46000, note: '印表機採購' },
  { id: 5, orderNo: 'PO-20250105', supplier: '捷元電腦', itemCount: 6, amount: 198000, note: '筆記型電腦採購' },
]

const item = demoData.find(d => d.id === id)
if (!item) {
  throw createError({ statusCode: 404, statusMessage: '找不到此採購單' })
}

const supplierOptions = ['大同資訊股份有限公司', '聯強國際', '全國電子', '震旦行', '捷元電腦']

const form = reactive({
  supplier: item.supplier,
  itemCount: item.itemCount,
  amount: item.amount,
  note: item.note,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新採購單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '採購單已更新（Demo）', color: 'success' })
    navigateTo('/purchase')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '採購管理', to: '/purchase' },
      { label: '編輯採購單' },
    ]" />

    <h1 class="text-2xl font-bold">編輯採購單 - {{ item.orderNo }}</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="供應商" required>
          <USelectMenu v-model="form.supplier" :items="supplierOptions" placeholder="選擇供應商" class="w-full" />
        </UFormField>

        <UFormField label="品項數" required>
          <UInput v-model="form.itemCount" type="number" placeholder="輸入品項數" class="w-full" />
        </UFormField>

        <UFormField label="金額" required>
          <UInput v-model="form.amount" type="number" placeholder="輸入金額" class="w-full" />
        </UFormField>

        <UFormField label="備註">
          <UTextarea v-model="form.note" placeholder="輸入備註" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/purchase" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
