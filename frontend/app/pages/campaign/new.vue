<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const form = reactive({
  name: '',
  type: '',
  budget: undefined as number | undefined,
  start_date: '',
  description: '',
})

const typeOptions = ['線上', '線下', '社群']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立行銷活動
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '活動已建立（Demo）', color: 'success' })
    navigateTo('/campaign')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '行銷活動', to: '/campaign' },
      { label: '新增活動' },
    ]" />

    <h1 class="text-2xl font-bold">新增活動</h1>

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
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
