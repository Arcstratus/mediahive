<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

const customerOptions = ['台灣科技股份有限公司', '大眾貿易有限公司', '永豐製造股份有限公司', '新創數位有限公司', '綠能環保科技公司']
const managerOptions = ['陳大文', '林小美', '王志明', '張雅婷', '李國華']

const form = reactive({
  name: '',
  customer: '',
  manager: '',
  start_date: '',
  end_date: '',
  description: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立專案
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '專案已建立（Demo）', color: 'success' })
    navigateTo('/project')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '專案管理', to: '/project' },
      { label: '新增專案' },
    ]" />

    <h1 class="text-2xl font-bold">新增專案</h1>

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
          <UButton label="取消" color="neutral" variant="outline" to="/project" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
