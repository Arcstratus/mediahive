<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

interface CampaignDetail {
  id: number
  name: string
  type: string
  budget: number
  start_date: string
  description: string
}

// TODO: 後端支援 - 從 API 取得行銷活動資料
const items: CampaignDetail[] = [
  { id: 1, name: '春季產品發表會', type: '線下', budget: 300000, start_date: '2024-03-15', description: '' },
  { id: 2, name: 'Facebook 廣告投放', type: '社群', budget: 150000, start_date: '2024-05-01', description: '' },
  { id: 3, name: '線上研討會 - AI 趨勢', type: '線上', budget: 50000, start_date: '2024-06-20', description: '' },
  { id: 4, name: '年中促銷 EDM', type: '線上', budget: 80000, start_date: '2024-07-01', description: '' },
  { id: 5, name: '產業博覽會參展', type: '線下', budget: 500000, start_date: '2024-09-10', description: '' },
]

const id = Number(route.params.id)
const campaign = items.find(item => item.id === id)

if (!campaign) {
  throw createError({ statusCode: 404, statusMessage: '找不到此活動' })
}

const form = reactive({
  name: campaign.name,
  type: campaign.type,
  budget: campaign.budget,
  start_date: campaign.start_date,
  description: campaign.description,
})

const typeOptions = ['線上', '線下', '社群']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新行銷活動
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '活動已更新（Demo）', color: 'success' })
    navigateTo('/campaign')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '行銷活動', to: '/campaign' },
      { label: '編輯活動' },
    ]" />

    <h1 class="text-2xl font-bold">編輯活動</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="活動名稱" required>
          <UInput v-model="form.name" placeholder="輸入活動名稱" class="w-full" />
        </UFormField>

        <UFormField label="類型">
          <USelectMenu v-model="form.type" :items="typeOptions" placeholder="選擇類型" class="w-full" />
        </UFormField>

        <UFormField label="預算">
          <UInput v-model="form.budget" type="number" placeholder="輸入預算金額" class="w-full" />
        </UFormField>

        <UFormField label="開始日期">
          <UInput v-model="form.start_date" type="date" class="w-full" />
        </UFormField>

        <UFormField label="說明">
          <UTextarea v-model="form.description" placeholder="輸入活動說明" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/campaign" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
