<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  customer: '',
  amount: null as number | null,
  start_date: '',
  end_date: '',
  description: '',
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
  // TODO: 後端支援 - 呼叫 API 建立合約
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '合約已建立（Demo）', color: 'success' })
    navigateTo('/contract')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '合約管理', to: '/contract' },
      { label: '新增合約' },
    ]" />

    <h1 class="text-2xl font-bold">新增合約</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
