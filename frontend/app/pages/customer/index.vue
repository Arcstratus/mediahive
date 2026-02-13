<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoCustomer, CustomerLevel, CustomerStatus, CustomerIndustry } from '~/types'

definePageMeta({ layout: 'dashboard' })

const { customers, getPrimaryContact } = useDemoCustomers()

const search = ref('')
const filterLevel = ref<CustomerLevel | ''>('')
const filterStatus = ref<CustomerStatus | ''>('')
const filterIndustry = ref<CustomerIndustry | ''>('')

const levelOptions = [{ label: '全部等級', value: '' }, { label: 'VIP', value: 'VIP' }, { label: '一般', value: '一般' }, { label: '潛在', value: '潛在' }]
const statusOptions = [{ label: '全部狀態', value: '' }, { label: '啟用', value: 'active' }, { label: '停用', value: 'inactive' }]
const industryOptions = [
  { label: '全部產業', value: '' },
  { label: '資訊科技', value: '資訊科技' },
  { label: '國際貿易', value: '國際貿易' },
  { label: '製造業', value: '製造業' },
  { label: '數位媒體', value: '數位媒體' },
  { label: '環保科技', value: '環保科技' },
  { label: '金融業', value: '金融業' },
  { label: '零售業', value: '零售業' },
  { label: '其他', value: '其他' },
]

const filteredCustomers = computed(() => {
  return customers.value.filter((c) => {
    if (search.value) {
      const q = search.value.toLowerCase()
      const matchSearch = c.name.toLowerCase().includes(q)
        || c.short_name.toLowerCase().includes(q)
        || c.tax_id.includes(q)
      if (!matchSearch) return false
    }
    if (filterLevel.value && c.level !== filterLevel.value) return false
    if (filterStatus.value && c.status !== filterStatus.value) return false
    if (filterIndustry.value && c.industry !== filterIndustry.value) return false
    return true
  })
})

const columns: TableColumn<DemoCustomer>[] = [
  { accessorKey: 'name', header: '客戶名稱' },
  { accessorKey: 'short_name', header: '簡稱' },
  { accessorKey: 'industry', header: '產業' },
  { id: 'primary_contact', header: '主要聯絡人' },
  { accessorKey: 'phone', header: '電話' },
  { id: 'level', accessorKey: 'level', header: '等級' },
  { id: 'status', accessorKey: 'status', header: '狀態' },
  { id: 'actions', header: '' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '客戶管理' }]" />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">客戶管理</h1>
      <UButton label="新增客戶" icon="i-lucide-plus" to="/customer/new" />
    </div>

    <!-- 搜尋與篩選 -->
    <div class="flex flex-wrap items-center gap-3">
      <UInput
        v-model="search"
        placeholder="搜尋名稱、簡稱、統編..."
        icon="i-lucide-search"
        class="w-64"
      />
      <USelectMenu
        v-model="filterLevel"
        :items="levelOptions"
        value-key="value"
        class="w-32"
      />
      <USelectMenu
        v-model="filterStatus"
        :items="statusOptions"
        value-key="value"
        class="w-32"
      />
      <USelectMenu
        v-model="filterIndustry"
        :items="industryOptions"
        value-key="value"
        class="w-36"
      />
    </div>

    <UTable :data="filteredCustomers" :columns="columns">
      <template #name-cell="{ row }">
        <NuxtLink
          :to="`/customer/${row.original.id}`"
          class="text-primary hover:underline font-medium"
        >
          {{ row.original.name }}
        </NuxtLink>
      </template>

      <template #primary_contact-cell="{ row }">
        {{ getPrimaryContact(row.original.id)?.name ?? '-' }}
      </template>

      <template #level-cell="{ row }">
        <UBadge
          :label="row.original.level"
          :color="(customerLevelColorMap[row.original.level] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #status-cell="{ row }">
        <UBadge
          :label="row.original.status === 'active' ? '啟用' : '停用'"
          :color="(customerStatusColorMap[row.original.status] as any) ?? 'neutral'"
          variant="subtle"
          size="sm"
        />
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-eye"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/customer/${row.original.id}`"
          />
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/customer/${row.original.id}/edit`"
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
