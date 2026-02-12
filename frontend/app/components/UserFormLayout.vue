<script setup lang="ts">
const props = defineProps<{
  title: string
  avatar?: string
  name: string
  email: string
  phone: string
  department: string
  role: string
  status: 'active' | 'inactive'
  loading?: boolean
}>()

const emit = defineEmits<{
  'update:name': [value: string]
  'update:email': [value: string]
  'update:phone': [value: string]
  'update:department': [value: string]
  'update:role': [value: string]
  'update:status': [value: 'active' | 'inactive']
  'submit': []
}>()

const roleOptions = [
  { label: '系統管理員', value: '系統管理員' },
  { label: '部門主管', value: '部門主管' },
  { label: '一般使用者', value: '一般使用者' },
]

const statusOptions = [
  { label: '啟用', value: 'active' },
  { label: '停用', value: 'inactive' },
]

// TODO: 後端支援 - 從 API 取得部門列表
const departmentOptions = [
  { label: '資訊部', value: '資訊部' },
  { label: '人資部', value: '人資部' },
  { label: '業務部', value: '業務部' },
  { label: '財務部', value: '財務部' },
  { label: '研發部', value: '研發部' },
]
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl font-bold">{{ title }}</h1>

    <div class="grid grid-cols-3 gap-6">
      <!-- Left: Avatar -->
      <div class="col-span-1">
        <UCard>
          <div class="flex flex-col items-center gap-4 py-4">
            <UAvatar
              :src="avatar || undefined"
              icon="i-lucide-user"
              size="3xl"
            />
            <!-- TODO: 後端支援 - 實作頭像上傳功能 -->
            <UButton label="上傳照片" icon="i-lucide-upload" variant="soft" disabled />
            <p class="text-xs text-muted">支援 JPG、PNG，建議 200x200 以上</p>
          </div>
        </UCard>
      </div>

      <!-- Right: Form -->
      <div class="col-span-2">
        <UCard>
          <form class="flex flex-col gap-4" @submit.prevent="emit('submit')">
            <UFormField label="名稱">
              <UInput
                :model-value="name"
                placeholder="請輸入姓名"
                icon="i-lucide-user"
                @update:model-value="emit('update:name', $event as string)"
              />
            </UFormField>

            <UFormField label="電子郵件">
              <UInput
                :model-value="email"
                type="email"
                placeholder="請輸入電子郵件"
                icon="i-lucide-mail"
                @update:model-value="emit('update:email', $event as string)"
              />
            </UFormField>

            <UFormField label="電話">
              <UInput
                :model-value="phone"
                placeholder="請輸入電話號碼"
                icon="i-lucide-phone"
                @update:model-value="emit('update:phone', $event as string)"
              />
            </UFormField>

            <UFormField label="部門">
              <USelectMenu
                :model-value="department"
                :items="departmentOptions"
                value-key="value"
                placeholder="請選擇部門"
                @update:model-value="emit('update:department', $event as string)"
              />
            </UFormField>

            <UFormField label="角色">
              <USelectMenu
                :model-value="role"
                :items="roleOptions"
                value-key="value"
                placeholder="請選擇角色"
                @update:model-value="emit('update:role', $event as string)"
              />
            </UFormField>

            <UFormField label="狀態">
              <USelectMenu
                :model-value="status"
                :items="statusOptions"
                value-key="value"
                placeholder="請選擇狀態"
                @update:model-value="emit('update:status', $event as 'active' | 'inactive')"
              />
            </UFormField>

            <div class="flex justify-end gap-2 pt-4">
              <UButton label="取消" variant="outline" color="neutral" to="/foundation/user" />
              <UButton type="submit" :label="loading ? '儲存中...' : '儲存'" icon="i-lucide-save" :loading="loading" />
            </div>
          </form>
        </UCard>
      </div>
    </div>
  </div>
</template>
