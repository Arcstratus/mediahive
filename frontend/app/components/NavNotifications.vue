<script setup lang="ts">
// TODO: 後端支援 - 從 API 取得使用者通知列表
const notifications = ref([
  {
    id: 1,
    title: '系統更新',
    description: '系統已更新至最新版本 v2.1.0',
    time: '5 分鐘前',
    read: false,
  },
  {
    id: 2,
    title: '新資源上傳',
    description: '已成功上傳 3 個檔案至資源庫',
    time: '30 分鐘前',
    read: false,
  },
  {
    id: 3,
    title: '排程備份完成',
    description: '每日自動備份已順利完成',
    time: '2 小時前',
    read: true,
  },
  {
    id: 4,
    title: '新使用者註冊',
    description: 'user@example.com 已完成帳號註冊',
    time: '昨天',
    read: true,
  },
])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)
</script>

<template>
  <UPopover :content="{ align: 'end' }">
    <div class="relative">
      <UButton
        icon="i-lucide-bell"
        variant="ghost"
        color="neutral"
        aria-label="通知"
      />
      <UBadge
        v-if="unreadCount > 0"
        :label="String(unreadCount)"
        color="error"
        size="xs"
        variant="solid"
        class="absolute -top-1 -right-1 min-w-4 justify-center !px-0.5 pointer-events-none"
      />
    </div>

    <template #content>
      <div class="w-80">
        <div class="flex items-center justify-between px-4 py-3 border-b border-default">
          <span class="font-semibold">通知</span>
          <UBadge v-if="unreadCount > 0" :label="`${unreadCount} 則未讀`" variant="subtle" size="xs" />
        </div>
        <div class="max-h-80 overflow-y-auto">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="px-4 py-3 hover:bg-elevated cursor-pointer border-b border-default last:border-0"
            :class="{ 'bg-elevated/50': !notification.read }"
          >
            <div class="flex items-start justify-between gap-2">
              <div class="flex-1 min-w-0">
                <p class="font-medium text-sm truncate">{{ notification.title }}</p>
                <p class="text-xs text-muted mt-0.5">{{ notification.description }}</p>
              </div>
              <span v-if="!notification.read" class="size-2 rounded-full bg-primary shrink-0 mt-1.5" />
            </div>
            <p class="text-xs text-dimmed mt-1">{{ notification.time }}</p>
          </div>
        </div>
      </div>
    </template>
  </UPopover>
</template>
