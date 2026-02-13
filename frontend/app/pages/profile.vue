<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const toast = useToast()

// TODO: 後端支援 - 從 API 取得目前登入使用者資訊
const profile = reactive({
  name: '王小明',
  email: 'xiaoming@example.com',
  phone: '0912-345-678',
  department: '資訊部',
  role: '系統管理員',
  avatar: '',
  bio: '負責系統維運與架構規劃',
})

const loading = ref(false)

async function onSubmit() {
  // TODO: 後端支援 - 呼叫 API 更新個人資料
  loading.value = true
  setTimeout(() => {
    loading.value = false
    toast.add({ title: '個人資料已更新（Demo）', color: 'success' })
  }, 800)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageBreadcrumb :items="[{ label: '個人資料' }]" />

    <!-- Banner + Avatar -->
    <div class="relative">
      <div class="h-40 rounded-lg bg-gradient-to-r from-primary/80 to-primary/40" />
      <div class="absolute -bottom-10 left-8 flex items-end gap-4">
        <UAvatar
          :src="profile.avatar || undefined"
          icon="i-lucide-user"
          size="3xl"
          class="ring-4 ring-default bg-default"
        />
        <div class="mb-2">
          <h1 class="text-xl font-bold">{{ profile.name }}</h1>
          <p class="text-sm text-muted">{{ profile.role }} · {{ profile.department }}</p>
        </div>
      </div>
    </div>

    <div class="h-6" />

    <!-- Content: Info Cards (1/3) + Edit Form (2/3) -->
    <div class="grid grid-cols-3 gap-6">
      <!-- Left: Info Cards -->
      <div class="col-span-1 flex flex-col gap-4">
        <UCard>
          <div class="flex flex-col gap-3">
            <h3 class="font-semibold text-sm text-muted">基本資訊</h3>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-mail" class="size-4 text-muted" />
              <span class="text-sm">{{ profile.email }}</span>
            </div>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-phone" class="size-4 text-muted" />
              <span class="text-sm">{{ profile.phone }}</span>
            </div>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-building" class="size-4 text-muted" />
              <span class="text-sm">{{ profile.department }}</span>
            </div>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-shield" class="size-4 text-muted" />
              <span class="text-sm">{{ profile.role }}</span>
            </div>
          </div>
        </UCard>

        <UCard>
          <div class="flex flex-col gap-3">
            <h3 class="font-semibold text-sm text-muted">關於我</h3>
            <p class="text-sm">{{ profile.bio || '尚未填寫' }}</p>
          </div>
        </UCard>
      </div>

      <!-- Right: Edit Form -->
      <div class="col-span-2">
        <UCard>
          <template #header>
            <h2 class="font-semibold">編輯個人資料</h2>
          </template>

          <form class="flex flex-col gap-4" @submit.prevent="onSubmit">
            <UFormField label="名稱">
              <UInput v-model="profile.name" placeholder="請輸入姓名" icon="i-lucide-user" />
            </UFormField>

            <UFormField label="電子郵件">
              <UInput v-model="profile.email" type="email" placeholder="請輸入電子郵件" icon="i-lucide-mail" />
            </UFormField>

            <UFormField label="電話">
              <UInput v-model="profile.phone" placeholder="請輸入電話號碼" icon="i-lucide-phone" />
            </UFormField>

            <UFormField label="關於我">
              <UTextarea v-model="profile.bio" placeholder="簡短自我介紹..." />
            </UFormField>

            <div class="flex justify-end pt-4">
              <UButton type="submit" label="儲存" icon="i-lucide-save" :loading="loading" />
            </div>
          </form>
        </UCard>
      </div>
    </div>
  </div>
</template>
