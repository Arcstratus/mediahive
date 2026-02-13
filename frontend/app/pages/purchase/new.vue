<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const supplierOptions = ['大同資訊股份有限公司', '聯強國際', '全國電子', '震旦行', '捷元電腦']

const form = reactive({
  supplier: '',
  itemCount: null as number | null,
  amount: null as number | null,
  note: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立採購單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '採購單已建立（Demo）', color: 'success' })
    navigateTo('/purchase')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '採購管理', to: '/purchase' },
      { label: '新增採購單' },
    ]" />

    <h1 class="text-2xl font-bold">新增採購單</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
