<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']

const form = reactive({
  customer: '',
  amount: '',
  due_date: '',
  note: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立請款
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '請款已建立（Demo）', color: 'success' })
    navigateTo('/invoice')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '請款管理', to: '/invoice' },
      { label: '新增請款' },
    ]" />

    <h1 class="text-2xl font-bold">新增請款</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
