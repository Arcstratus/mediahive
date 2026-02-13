<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const { findById } = useDemoCustomers()

const id = Number(route.params.id)
const customer = findById(id)

if (!customer) {
  throw createError({ statusCode: 404, statusMessage: '找不到此客戶' })
}

const form = reactive({
  name: customer.name,
  contact: customer.contact,
  email: customer.email,
  phone: customer.phone,
  industry: customer.industry,
  level: customer.level,
})

const industryOptions = ['資訊科技', '國際貿易', '製造業', '數位媒體', '環保科技', '金融業']
const levelOptions = ['VIP', '一般', '潛在']

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新客戶資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '客戶已更新（Demo）', color: 'success' })
    navigateTo('/customer')
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: '編輯客戶' },
    ]" />

    <h1 class="text-2xl font-bold">編輯客戶</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <UFormField label="客戶名稱" required>
          <UInput v-model="form.name" placeholder="輸入客戶名稱" class="w-full" />
        </UFormField>

        <UFormField label="聯絡人" required>
          <UInput v-model="form.contact" placeholder="輸入聯絡人" class="w-full" />
        </UFormField>

        <UFormField label="電子郵件" required>
          <UInput v-model="form.email" type="email" placeholder="輸入電子郵件" class="w-full" />
        </UFormField>

        <UFormField label="電話">
          <UInput v-model="form.phone" placeholder="輸入電話號碼" class="w-full" />
        </UFormField>

        <UFormField label="產業">
          <USelectMenu v-model="form.industry" :items="industryOptions" placeholder="選擇產業" class="w-full" />
        </UFormField>

        <UFormField label="等級">
          <USelectMenu v-model="form.level" :items="levelOptions" placeholder="選擇等級" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" to="/customer" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
