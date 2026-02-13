<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得商機資料
const items = [
  { id: 1, name: 'ERP 系統導入專案', customer: '台灣科技股份有限公司', amount: 'NT$ 1,200,000', stage: '報價中', owner: '陳業務', expected_close: '2024-06-30' },
  { id: 2, name: '年度維護合約續約', customer: '大眾貿易有限公司', amount: 'NT$ 360,000', stage: '議價中', owner: '林經理', expected_close: '2024-05-15' },
  { id: 3, name: '雲端遷移服務', customer: '永豐製造股份有限公司', amount: 'NT$ 850,000', stage: '需求確認', owner: '王顧問', expected_close: '2024-08-20' },
  { id: 4, name: '品牌官網改版', customer: '新創數位有限公司', amount: 'NT$ 480,000', stage: '初步接洽', owner: '張業務', expected_close: '2024-09-10' },
  { id: 5, name: '智慧工廠方案', customer: '綠能環保科技公司', amount: 'NT$ 2,500,000', stage: '已成交', owner: '陳業務', expected_close: '2024-04-01' },
]

const opportunity = items.find(item => item.id === id)

if (!opportunity) {
  throw createError({ statusCode: 404, statusMessage: '找不到此商機' })
}

const form = reactive({
  name: opportunity.name,
  customer: opportunity.customer,
  amount: opportunity.amount,
  stage: opportunity.stage,
  owner: opportunity.owner,
  expected_close: opportunity.expected_close,
})

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']
const stageOptions = ['初步接洽', '需求確認', '報價中', '議價中', '已成交']
const ownerOptions = ['陳業務', '林經理', '王顧問', '張業務', '李主管']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新商機
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '商機已更新（Demo）', color: 'success' })
    navigateTo('/opportunity')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '商機管理', to: '/opportunity' },
      { label: '編輯商機' },
    ]" />

    <h1 class="text-2xl font-bold">編輯商機</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="商機名稱" required>
          <UInput v-model="form.name" placeholder="輸入商機名稱" class="w-full" />
        </UFormField>

        <UFormField label="客戶">
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="預估金額">
          <UInput v-model="form.amount" placeholder="輸入預估金額" class="w-full" />
        </UFormField>

        <UFormField label="階段">
          <USelectMenu v-model="form.stage" :items="stageOptions" placeholder="選擇階段" class="w-full" />
        </UFormField>

        <UFormField label="負責人">
          <USelectMenu v-model="form.owner" :items="ownerOptions" placeholder="選擇負責人" class="w-full" />
        </UFormField>

        <UFormField label="預計成交日">
          <UInput v-model="form.expected_close" type="date" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/opportunity" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
