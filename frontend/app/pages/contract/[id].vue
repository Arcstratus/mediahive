<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

interface ContractData {
  id: number
  customer: string
  amount: number
  start_date: string
  end_date: string
  description: string
}

// TODO: 後端支援 - 從 API 取得合約資料
const contracts: ContractData[] = [
  { id: 1, customer: '台灣科技股份有限公司', amount: 1200000, start_date: '2024-01-01', end_date: '2024-12-31', description: '' },
  { id: 2, customer: '大眾貿易有限公司', amount: 360000, start_date: '2024-03-01', end_date: '2025-02-28', description: '' },
  { id: 3, customer: '永豐製造股份有限公司', amount: 720000, start_date: '2023-06-01', end_date: '2024-05-31', description: '' },
  { id: 4, customer: '新創數位有限公司', amount: 180000, start_date: '2023-01-01', end_date: '2023-12-31', description: '' },
  { id: 5, customer: '綠能環保科技公司', amount: 2500000, start_date: '2024-04-01', end_date: '2026-03-31', description: '' },
]

const id = Number(route.params.id)
const contract = contracts.find(c => c.id === id)

if (!contract) {
  throw createError({ statusCode: 404, statusMessage: '找不到此合約' })
}

const form = reactive({
  customer: contract.customer,
  amount: contract.amount,
  start_date: contract.start_date,
  end_date: contract.end_date,
  description: contract.description,
})

const customerOptions = [
  '台灣科技股份有限公司',
  '大眾貿易有限公司',
  '永豐製造股份有限公司',
  '新創數位有限公司',
  '綠能環保科技公司',
]

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新合約資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '合約已更新（Demo）', color: 'success' })
    navigateTo('/contract')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '合約管理', to: '/contract' },
      { label: '編輯合約' },
    ]" />

    <h1 class="text-2xl font-bold">編輯合約</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="客戶" required>
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="金額">
          <UInput v-model="form.amount" type="number" placeholder="輸入金額" class="w-full" />
        </UFormField>

        <UFormField label="起始日">
          <UInput v-model="form.start_date" type="date" class="w-full" />
        </UFormField>

        <UFormField label="到期日">
          <UInput v-model="form.end_date" type="date" class="w-full" />
        </UFormField>

        <UFormField label="說明">
          <UTextarea v-model="form.description" placeholder="輸入說明" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/contract" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
