<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()
const loading = ref(false)

// TODO: 後端支援 - 從 API 載入系統設定
const settings = reactive({
  siteName: 'Mediahive',
  siteDescription: '企業數位資產管理平台',
  maintenanceMode: false,
  allowRegistration: true,
  maxUploadSize: 100,
  sessionTimeout: 30,
  smtpHost: 'smtp.example.com',
  smtpPort: 587,
  smtpUser: 'noreply@example.com',
})

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 儲存系統設定
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '設定已儲存（Demo）', color: 'success' })
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '系統設定' }]" />

    <h1 class="text-2xl font-bold">系統設定</h1>

    <form class="flex flex-col gap-6 max-w-2xl" @submit.prevent="onSubmit">
      <UCard>
        <template #header>
          <h2 class="font-semibold">一般設定</h2>
        </template>
        <div class="flex flex-col gap-4">
          <UFormField label="網站名稱">
            <UInput v-model="settings.siteName" icon="i-lucide-globe" />
          </UFormField>
          <UFormField label="網站描述">
            <UTextarea v-model="settings.siteDescription" />
          </UFormField>
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium">維護模式</p>
              <p class="text-sm text-muted">啟用後僅管理員可存取系統</p>
            </div>
            <USwitch v-model="settings.maintenanceMode" />
          </div>
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium">開放註冊</p>
              <p class="text-sm text-muted">允許新使用者自行註冊帳號</p>
            </div>
            <USwitch v-model="settings.allowRegistration" />
          </div>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h2 class="font-semibold">安全性設定</h2>
        </template>
        <div class="flex flex-col gap-4">
          <UFormField label="最大上傳大小 (MB)">
            <UInput v-model.number="settings.maxUploadSize" type="number" icon="i-lucide-hard-drive" />
          </UFormField>
          <UFormField label="Session 逾時 (分鐘)">
            <UInput v-model.number="settings.sessionTimeout" type="number" icon="i-lucide-clock" />
          </UFormField>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h2 class="font-semibold">郵件設定</h2>
        </template>
        <div class="flex flex-col gap-4">
          <UFormField label="SMTP 伺服器">
            <UInput v-model="settings.smtpHost" icon="i-lucide-server" />
          </UFormField>
          <UFormField label="SMTP 連接埠">
            <UInput v-model.number="settings.smtpPort" type="number" />
          </UFormField>
          <UFormField label="SMTP 帳號">
            <UInput v-model="settings.smtpUser" icon="i-lucide-mail" />
          </UFormField>
        </div>
      </UCard>

      <div class="flex justify-end">
        <UButton type="submit" label="儲存設定" icon="i-lucide-save" :loading="loading" />
      </div>
    </form>
  </div>
</template>
