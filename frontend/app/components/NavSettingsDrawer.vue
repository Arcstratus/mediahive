<script setup lang="ts">
const colorMode = useColorMode()

const isDark = computed({
  get: () => colorMode.preference === 'dark',
  set: (value: boolean) => {
    colorMode.preference = value ? 'dark' : 'light'
  },
})

// TODO: 後端支援 - 從 API 載入與儲存使用者偏好設定
</script>

<template>
  <USlideover side="right" title="設定">
    <UButton
      icon="i-lucide-settings"
      variant="ghost"
      color="neutral"
      aria-label="設定"
    />

    <template #body>
      <div class="flex flex-col gap-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-moon" class="size-5" />
            <span class="font-medium">深色模式</span>
          </div>
          <USwitch v-model="isDark" />
        </div>

        <!-- TODO: 後端支援 - 未來可加入語言切換、通知偏好等設定 -->
      </div>
    </template>
  </USlideover>
</template>
