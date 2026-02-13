<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

interface TicketDemo {
  id: number
  customer: string
  subject: string
  priority: string
  description: string
}

const demoItems: TicketDemo[] = [
  { id: 1, customer: '台灣科技股份有限公司', subject: '系統登入異常', priority: '高', description: '使用者反映無法正常登入系統，已嘗試重設密碼但問題仍存在。' },
  { id: 2, customer: '大眾貿易有限公司', subject: '報表匯出格式錯誤', priority: '中', description: '匯出 Excel 報表時，部分欄位格式異常，數值顯示為文字。' },
  { id: 3, customer: '永豐製造股份有限公司', subject: '請求新增使用者帳號', priority: '低', description: '新進員工需要開通系統帳號，共 3 位使用者。' },
  { id: 4, customer: '新創數位有限公司', subject: 'API 串接技術支援', priority: '中', description: '客戶端工程師在串接訂單 API 時遇到驗證問題，需要協助排除。' },
  { id: 5, customer: '綠能環保科技公司', subject: '合約到期續約諮詢', priority: '低', description: '客戶詢問合約續約方案與價格調整事宜。' },
]

const id = Number(route.params.id)
const ticket = demoItems.find(item => item.id === id)

if (!ticket) {
  throw createError({ statusCode: 404, statusMessage: '找不到此工單' })
}

const form = reactive({
  customer: ticket.customer,
  subject: ticket.subject,
  priority: ticket.priority,
  description: ticket.description,
})

const customerOptions = [
  '台灣科技股份有限公司',
  '大眾貿易有限公司',
  '永豐製造股份有限公司',
  '新創數位有限公司',
  '綠能環保科技公司',
]

const priorityOptions = ['高', '中', '低']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新工單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '工單已更新（Demo）', color: 'success' })
    navigateTo('/ticket')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客服工單', to: '/ticket' },
      { label: '編輯工單' },
    ]" />

    <h1 class="text-2xl font-bold">編輯工單</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="客戶" required>
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="主旨" required>
          <UInput v-model="form.subject" placeholder="輸入主旨" class="w-full" />
        </UFormField>

        <UFormField label="優先度">
          <USelectMenu v-model="form.priority" :items="priorityOptions" placeholder="選擇優先度" class="w-full" />
        </UFormField>

        <UFormField label="說明">
          <UTextarea v-model="form.description" placeholder="輸入說明" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/ticket" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
