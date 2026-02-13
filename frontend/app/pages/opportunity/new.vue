<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  name: '',
  customer: '',
  amount: '',
  stage: '',
  owner: '',
  expected_close: '',
})

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']
const stageOptions = ['初步接洽', '需求確認', '報價中', '議價中']
const ownerOptions = ['陳業務', '林經理', '王顧問', '張業務', '李主管']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立商機
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '商機已建立（Demo）', color: 'success' })
    navigateTo('/opportunity')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '商機管理', to: '/opportunity' },
      { label: '新增商機' },
    ]" />

    <h1 class="text-2xl font-bold">新增商機</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="商機名稱" required>
          <UInput v-model="form.name" placeholder="輸入商機名稱" class="w-full" />
        </UFormField>

        <UFormField label="客戶">
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="預估金額">
          <UInput v-model="form.amount" type="number" placeholder="輸入預估金額" class="w-full" />
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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
