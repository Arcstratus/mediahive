<script setup lang="ts">
// TODO: 後端支援 - 從 API 取得目前登入使用者資訊
const user = ref({
  name: '王小明',
  email: 'xiaoming@example.com',
  avatar: '',
})
</script>

<template>
  <USlideover side="right" title="個人資訊">
    <UButton variant="ghost" color="neutral" class="rounded-full" aria-label="使用者選單">
      <UAvatar
        :src="user.avatar || undefined"
        icon="i-lucide-user"
        size="sm"
      />
    </UButton>

    <template #body>
      <div class="flex flex-col items-center gap-4 py-4">
        <UAvatar
          :src="user.avatar || undefined"
          icon="i-lucide-user"
          size="3xl"
        />
        <div class="text-center">
          <h3 class="text-lg font-semibold">{{ user.name }}</h3>
          <p class="text-sm text-muted">{{ user.email }}</p>
        </div>
      </div>

      <!-- TODO: 後端支援 - 加入登出、修改密碼等功能 -->
    </template>
  </USlideover>
</template>
