<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得報價資料
const quote = {
  id,
  quoteNo: `QT-2025010${id}`,
  customer: '台灣科技股份有限公司',
  valid_until: '2025-03-31',
  note: 'ERP 系統導入專案報價',
}

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']

const form = reactive({
  customer: quote.customer,
  valid_until: quote.valid_until,
  note: quote.note,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新報價
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '報價已更新（Demo）', color: 'success' })
    navigateTo('/quote')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '報價管理', to: '/quote' },
      { label: '編輯報價' },
    ]" />

    <h1 class="text-2xl font-bold">編輯報價 - {{ quote.quoteNo }}</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="客戶" required>
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="有效期限">
          <UInput v-model="form.valid_until" type="date" class="w-full" />
        </UFormField>

        <UFormField label="備註">
          <UTextarea v-model="form.note" placeholder="輸入備註" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/quote" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
