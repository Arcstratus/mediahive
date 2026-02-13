<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const customerId = Number(route.params.id)
const contactId = Number(route.params.contactId)

const { findById, findContactById } = useDemoCustomers()

const customer = findById(customerId)
if (!customer) {
  throw createError({ statusCode: 404, statusMessage: '找不到此客戶' })
}

const contact = findContactById(contactId)
if (!contact || contact.customerId !== customerId) {
  throw createError({ statusCode: 404, statusMessage: '找不到此聯絡人' })
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[
      { label: '客戶管理', to: '/customer' },
      { label: customer.name, to: `/customer/${customerId}` },
      { label: contact.name },
    ]" />

    <!-- 標頭 -->
    <div class="flex items-center gap-3">
      <h1 class="text-2xl font-bold">{{ contact.name }}</h1>
      <UBadge
        v-if="contact.is_primary"
        label="主要聯絡人"
        color="info"
        variant="subtle"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 聯絡資訊 -->
      <UCard>
        <template #header>
          <h3 class="font-semibold">聯絡資訊</h3>
        </template>
        <dl class="flex flex-col gap-3">
          <div v-if="contact.email" class="flex justify-between">
            <dt class="text-muted">電子郵件</dt>
            <dd>
              <a :href="`mailto:${contact.email}`" class="text-primary hover:underline">{{ contact.email }}</a>
            </dd>
          </div>
          <div v-if="contact.phone" class="flex justify-between">
            <dt class="text-muted">電話</dt>
            <dd>{{ contact.phone }}</dd>
          </div>
          <div v-if="contact.mobile" class="flex justify-between">
            <dt class="text-muted">手機</dt>
            <dd>{{ contact.mobile }}</dd>
          </div>
        </dl>
      </UCard>

      <!-- 屬性 -->
      <UCard>
        <template #header>
          <h3 class="font-semibold">屬性</h3>
        </template>
        <dl class="flex flex-col gap-3">
          <div class="flex justify-between">
            <dt class="text-muted">職稱</dt>
            <dd>{{ contact.title || '-' }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">所屬客戶</dt>
            <dd>
              <NuxtLink :to="`/customer/${customerId}`" class="text-primary hover:underline">
                {{ customer.name }}
              </NuxtLink>
            </dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">建立時間</dt>
            <dd>{{ formatDate(contact.created_at) }}</dd>
          </div>
        </dl>
      </UCard>
    </div>

    <!-- 備註 -->
    <UCard v-if="contact.notes">
      <template #header>
        <h3 class="font-semibold">備註</h3>
      </template>
      <p class="text-sm whitespace-pre-wrap">{{ contact.notes }}</p>
    </UCard>
  </div>
</template>
