<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const customerId = Number(route.params.id)

const { findById } = useDemoCustomers()
const customer = findById(customerId)
if (!customer) {
  throw createError({ statusCode: 404, statusMessage: '找不到此客戶' })
}

const form = reactive({
  name: '',
  title: '',
  email: '',
  phone: '',
  mobile: '',
  is_primary: false,
  notes: '',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 建立聯絡人
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '聯絡人已建立（Demo）', color: 'success' })
    navigateTo(`/customer/${customerId}`)
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: customer.name, to: `/customer/${customerId}` },
      { label: '新增聯絡人' },
    ]" />

    <h1 class="text-2xl font-bold">新增聯絡人</h1>

    <UCard class="max-w-xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="姓名" required>
            <UInput v-model="form.name" placeholder="輸入姓名" class="w-full" />
          </UFormField>

          <UFormField label="職稱">
            <UInput v-model="form.title" placeholder="輸入職稱" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="電子郵件">
          <UInput v-model="form.email" type="email" placeholder="輸入電子郵件" class="w-full" />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="電話">
            <UInput v-model="form.phone" placeholder="輸入電話" class="w-full" />
          </UFormField>

          <UFormField label="手機">
            <UInput v-model="form.mobile" placeholder="輸入手機號碼" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="主要聯絡人">
          <UCheckbox v-model="form.is_primary" label="設為主要聯絡人" />
        </UFormField>

        <UFormField label="備註">
          <UTextarea v-model="form.notes" placeholder="輸入備註" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" :to="`/customer/${customerId}`" />
          <UButton label="建立" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
