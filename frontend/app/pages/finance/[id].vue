<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

const demoData = [
  { id: 1, type: '收入', account: '銷貨收入', amount: 520000, remark: '台積電訂單款項', date: '2025-01-10' },
  { id: 2, type: '支出', account: '辦公用品', amount: 15200, remark: '採購文具與耗材', date: '2025-01-09' },
  { id: 3, type: '支出', account: '設備折舊', amount: 38000, remark: '一月份設備折舊攤提', date: '2025-01-08' },
  { id: 4, type: '收入', account: '利息收入', amount: 4800, remark: '活期存款利息', date: '2025-01-07' },
  { id: 5, type: '支出', account: '人事費用', amount: 1250000, remark: '一月份薪資發放', date: '2025-01-06' },
]

const item = demoData.find(d => d.id === id)

if (!item) {
  throw createError({ statusCode: 404, statusMessage: '找不到此傳票' })
}

const form = reactive({
  type: item.type,
  account: item.account,
  amount: item.amount,
  remark: item.remark,
  date: item.date,
})

const typeOptions = ['收入', '支出']
const accountOptions = ['銷貨收入', '辦公用品', '設備折舊', '利息收入', '人事費用']

const loading = ref(false)

async function onSubmit() {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '傳票已更新（Demo）', color: 'success' })
    navigateTo('/finance')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '財務會計', to: '/finance' }, { label: '編輯傳票' }]" />

    <h1 class="text-2xl font-bold">編輯傳票</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="類型" required>
          <USelectMenu v-model="form.type" :items="typeOptions" placeholder="選擇類型" class="w-full" />
        </UFormField>
        <UFormField label="科目" required>
          <USelectMenu v-model="form.account" :items="accountOptions" placeholder="選擇科目" class="w-full" />
        </UFormField>
        <UFormField label="金額" required>
          <UInput v-model.number="form.amount" type="number" placeholder="輸入金額" class="w-full" />
        </UFormField>
        <UFormField label="備註">
          <UTextarea v-model="form.remark" placeholder="輸入備註" class="w-full" />
        </UFormField>
        <UFormField label="日期" required>
          <UInput v-model="form.date" type="date" class="w-full" />
        </UFormField>
        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/finance" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
