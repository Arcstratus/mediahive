<script setup lang="ts">
import type { CustomerIndustry, CustomerLevel, CustomerStatus } from '~/types'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const id = Number(route.params.id)

const { findById } = useDemoCustomers()
const customer = findById(id)
if (!customer) {
  throw createError({ statusCode: 404, statusMessage: '找不到此客戶' })
}

const industryOptions: CustomerIndustry[] = ['資訊科技', '國際貿易', '製造業', '數位媒體', '環保科技', '金融業', '零售業', '其他']
const levelOptions: CustomerLevel[] = ['VIP', '一般', '潛在']
const statusOptions: CustomerStatus[] = ['active', 'inactive']

const form = reactive({
  name: customer.name,
  short_name: customer.short_name,
  tax_id: customer.tax_id,
  industry: customer.industry,
  level: customer.level,
  status: customer.status,
  address: customer.address,
  phone: customer.phone,
  fax: customer.fax,
  website: customer.website,
  notes: customer.notes,
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新客戶資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '客戶已更新（Demo）', color: 'success' })
    navigateTo(`/customer/${id}`)
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: customer.name, to: `/customer/${id}` },
      { label: '編輯' },
    ]" />

    <h1 class="text-2xl font-bold">編輯客戶</h1>

    <UCard class="max-w-2xl">
      <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="客戶名稱" required>
            <UInput v-model="form.name" placeholder="輸入客戶名稱" class="w-full" />
          </UFormField>

          <UFormField label="簡稱">
            <UInput v-model="form.short_name" placeholder="輸入簡稱" class="w-full" />
          </UFormField>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="統一編號">
            <UInput v-model="form.tax_id" placeholder="輸入統一編號" class="w-full" />
          </UFormField>

          <UFormField label="產業">
            <USelectMenu v-model="form.industry" :items="industryOptions" placeholder="選擇產業" class="w-full" />
          </UFormField>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="等級">
            <USelectMenu v-model="form.level" :items="levelOptions" placeholder="選擇等級" class="w-full" />
          </UFormField>

          <UFormField label="狀態">
            <USelectMenu v-model="form.status" :items="statusOptions" placeholder="選擇狀態" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="地址">
          <UInput v-model="form.address" placeholder="輸入地址" class="w-full" />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField label="公司電話">
            <UInput v-model="form.phone" placeholder="輸入公司電話" class="w-full" />
          </UFormField>

          <UFormField label="傳真">
            <UInput v-model="form.fax" placeholder="輸入傳真號碼" class="w-full" />
          </UFormField>
        </div>

        <UFormField label="網站">
          <UInput v-model="form.website" placeholder="輸入網站網址" class="w-full" />
        </UFormField>

        <UFormField label="備註">
          <UTextarea v-model="form.notes" placeholder="輸入備註" class="w-full" />
        </UFormField>

        <div class="flex justify-end gap-2 pt-2">
          <UButton label="取消" color="neutral" variant="outline" :to="`/customer/${id}`" />
          <UButton label="儲存" type="submit" :loading="loading" />
        </div>
      </form>
    </UCard>
  </div>
</template>
