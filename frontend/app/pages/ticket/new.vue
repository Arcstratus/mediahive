<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  customer: '',
  subject: '',
  priority: '',
  description: '',
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
  // TODO: 後端支援 - 呼叫 API 建立工單
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '工單已建立（Demo）', color: 'success' })
    navigateTo('/ticket')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客服工單', to: '/ticket' },
      { label: '新增工單' },
    ]" />

    <h1 class="text-2xl font-bold">新增工單</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
