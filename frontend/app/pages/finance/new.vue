<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  type: '',
  account: '',
  amount: 0,
  remark: '',
  date: '',
})

const typeOptions = ['收入', '支出']
const accountOptions = ['銷貨收入', '辦公用品', '設備折舊', '利息收入', '人事費用']

const loading = ref(false)

async function onSubmit() {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '傳票已建立（Demo）', color: 'success' })
    navigateTo('/finance')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '財務會計', to: '/finance' }, { label: '新增傳票' }]" />

    <h1 class="text-2xl font-bold">新增傳票</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
