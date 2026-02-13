<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得請款資料
const invoice = {
  id,
  invoiceNo: `INV-2025010${id}`,
  customer: '台灣科技股份有限公司',
  amount: 680000,
  due_date: '2025-02-15',
  note: 'ERP 系統導入專案請款',
}

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']

const form = reactive({
  customer: invoice.customer,
  amount: String(invoice.amount),
  due_date: invoice.due_date,
  note: invoice.note,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新請款
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '請款已更新（Demo）', color: 'success' })
    navigateTo('/invoice')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '請款管理', to: '/invoice' },
      { label: '編輯請款' },
    ]" />

    <h1 class="text-2xl font-bold">編輯請款 - {{ invoice.invoiceNo }}</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="客戶" required>
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="金額" required>
          <UInput v-model="form.amount" type="number" placeholder="輸入金額" icon="i-lucide-dollar-sign" class="w-full" />
        </UFormField>

        <UFormField label="付款期限">
          <UInput v-model="form.due_date" type="date" class="w-full" />
        </UFormField>

        <UFormField label="備註">
          <UTextarea v-model="form.note" placeholder="輸入備註" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/invoice" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
