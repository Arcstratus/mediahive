<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()

const id = Number(route.params.id)

// TODO: 後端支援 - 從 API 取得專案資料
const project = {
  id,
  name: 'ERP 系統導入',
  customer: '台灣科技股份有限公司',
  manager: '陳大文',
  start_date: '2025-01-01',
  end_date: '2025-06-30',
  description: '為客戶導入完整 ERP 系統，包含庫存、採購、銷售及財務模組。',
}

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']
const managerOptions = ['陳大文', '林小美', '王志明', '張雅婷', '李國華']

const form = reactive({
  name: project.name,
  customer: project.customer,
  manager: project.manager,
  start_date: project.start_date,
  end_date: project.end_date,
  description: project.description,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新專案
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '專案已更新（Demo）', color: 'success' })
    navigateTo(`/project/${id}`)
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: project.name, to: `/project/${id}` },
      { label: '編輯' },
    ]" />

    <h1 class="text-2xl font-bold">編輯專案</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="專案名稱" required>
          <UInput v-model="form.name" placeholder="輸入專案名稱" class="w-full" />
        </UFormField>

        <UFormField label="客戶" required>
          <USelectMenu v-model="form.customer" :items="customerOptions" placeholder="選擇客戶" class="w-full" />
        </UFormField>

        <UFormField label="專案經理">
          <USelectMenu v-model="form.manager" :items="managerOptions" placeholder="選擇專案經理" class="w-full" />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="開始日期">
            <UInput v-model="form.start_date" type="date" class="w-full" />
          </UFormField>

          <UFormField label="結束日期">
            <UInput v-model="form.end_date" type="date" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="說明">
          <UTextarea v-model="form.description" placeholder="輸入專案說明" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" :to="`/project/${id}`" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
