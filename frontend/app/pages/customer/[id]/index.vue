<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { DemoContact } from '~/types'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const toast = useToast()
const id = Number(route.params.id)

const { findById, getCustomerContacts } = useDemoCustomers()

const customer = findById(id)
if (!customer) {
  throw createError({ statusCode: 404, statusMessage: '找不到此客戶' })
}

const customerContacts = computed(() => getCustomerContacts(id))

const contactColumns: TableColumn<DemoContact>[] = [
  { accessorKey: 'name', header: '姓名' },
  { accessorKey: 'title', header: '職稱' },
  { accessorKey: 'email', header: '電子郵件' },
  { accessorKey: 'phone', header: '電話' },
  { accessorKey: 'mobile', header: '手機' },
  { id: 'is_primary', accessorKey: 'is_primary', header: '主要' },
  { id: 'actions', header: '' },
]

// 停用/啟用
const showStatusConfirm = ref(false)

function onToggleStatus() {
  showStatusConfirm.value = true
}

function confirmToggleStatus() {
  customer.status = customer.status === 'active' ? 'inactive' : 'active'
  showStatusConfirm.value = false
  toast.add({ title: `客戶已${customer.status === 'active' ? '啟用' : '停用'}（Demo）`, color: 'success' })
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: customer.name },
    ]" />

    <!-- 標頭 -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <h1 class="text-2xl font-bold">{{ customer.name }}</h1>
        <UBadge
          :label="customer.level"
          :color="(customerLevelColorMap[customer.level] as any) ?? 'neutral'"
          variant="subtle"
        />
        <UBadge
          :label="customer.status === 'active' ? '啟用' : '停用'"
          :color="(customerStatusColorMap[customer.status] as any) ?? 'neutral'"
          variant="subtle"
        />
      </div>
      <div class="flex items-center gap-2">
        <UButton
          label="編輯"
          icon="i-lucide-pencil"
          variant="outline"
          :to="`/customer/${id}/edit`"
        />
        <UButton
          :label="customer.status === 'active' ? '停用' : '啟用'"
          :icon="customer.status === 'active' ? 'i-lucide-ban' : 'i-lucide-check-circle'"
          :color="customer.status === 'active' ? 'error' : 'success'"
          variant="outline"
          @click="onToggleStatus"
        />
      </div>
    </div>

    <!-- 客戶資訊 + 備註 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">客戶資訊</h3>
        </template>
        <dl class="flex flex-col gap-3">
          <div class="flex justify-between">
            <dt class="text-muted">簡稱</dt>
            <dd>{{ customer.short_name }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">統一編號</dt>
            <dd>{{ customer.tax_id }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">產業</dt>
            <dd>{{ customer.industry }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">公司電話</dt>
            <dd>{{ customer.phone }}</dd>
          </div>
          <div v-if="customer.fax" class="flex justify-between">
            <dt class="text-muted">傳真</dt>
            <dd>{{ customer.fax }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">地址</dt>
            <dd>{{ customer.address }}</dd>
          </div>
          <div v-if="customer.website" class="flex justify-between">
            <dt class="text-muted">網站</dt>
            <dd>
              <a :href="customer.website" target="_blank" class="text-primary hover:underline">{{ customer.website }}</a>
            </dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">建立時間</dt>
            <dd>{{ formatDate(customer.created_at) }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">最後更新</dt>
            <dd>{{ formatDate(customer.updated_at) }}</dd>
          </div>
        </dl>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">備註</h3>
        </template>
        <p v-if="customer.notes" class="text-sm whitespace-pre-wrap">{{ customer.notes }}</p>
        <p v-else class="text-sm text-muted">無備註</p>
      </UCard>
    </div>

    <!-- 聯絡人區塊 -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">聯絡人</h3>
          <UButton label="新增聯絡人" icon="i-lucide-plus" size="sm" variant="outline" :to="`/customer/${id}/contacts/new`" />
        </div>
      </template>

      <UTable v-if="customerContacts.length" :data="customerContacts" :columns="contactColumns">
        <template #name-cell="{ row }">
          <NuxtLink
            :to="`/customer/${id}/contacts/${row.original.id}`"
            class="text-primary hover:underline font-medium"
          >
            {{ row.original.name }}
          </NuxtLink>
        </template>

        <template #is_primary-cell="{ row }">
          <UBadge
            v-if="row.original.is_primary"
            label="主要"
            color="info"
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
              :to="`/customer/${id}/contacts/${row.original.id}`"
            />
          </div>
        </template>
      </UTable>

      <div v-else class="text-center text-muted py-4">
        尚無聯絡人
      </div>
    </UCard>

    <!-- 相關紀錄 (placeholder) -->
    <UCard>
      <template #header>
        <h3 class="font-semibold">相關紀錄</h3>
      </template>
      <div class="text-center text-muted py-4">
        未來將顯示商機、合約、報價、請款等相關紀錄。
      </div>
    </UCard>

    <!-- 停用/啟用確認對話框 -->
    <UModal v-model:open="showStatusConfirm">
      <template #content>
        <UCard>
          <template #header>
            <h3 class="font-semibold">確認{{ customer.status === 'active' ? '停用' : '啟用' }}</h3>
          </template>
          <p class="text-sm">確定要將「{{ customer.name }}」{{ customer.status === 'active' ? '停用' : '啟用' }}嗎？</p>
          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton label="取消" color="neutral" variant="outline" @click="showStatusConfirm = false" />
              <UButton
                :label="customer.status === 'active' ? '確認停用' : '確認啟用'"
                :color="customer.status === 'active' ? 'error' : 'success'"
                @click="confirmToggleStatus"
              />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
