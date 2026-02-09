<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({
  layout: 'dashboard'
})

interface Resource {
  id: number
  type: string
  url: string | null
  title: string | null
  created_at: string
}

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

interface ScannedFile {
  path: string
  name: string
  type: 'image' | 'video'
  size: number
}

const { public: { apiBase } } = useRuntimeConfig()

const { data, refresh } = await useAsyncData<PaginatedResponse>('all-resources', () =>
  $fetch(`${apiBase}/resources`, { query: { per_page: 100 } })
)

const items = computed(() => data.value?.items ?? [])
const urlCount = computed(() => items.value.filter(r => r.type === 'url').length)
const imageCount = computed(() => items.value.filter(r => r.type === 'image').length)
const videoCount = computed(() => items.value.filter(r => r.type === 'video').length)

const cards = [
  { label: 'URLs', icon: 'i-lucide-link', to: '/resources/urls', count: urlCount },
  { label: 'Images', icon: 'i-lucide-image', to: '/resources/images', count: imageCount },
  { label: 'Videos', icon: 'i-lucide-video', to: '/resources/videos', count: videoCount }
]

// Import modal state
const importOpen = ref(false)
const folderPath = ref('')
const scannedFiles = ref<ScannedFile[]>([])
const scanned = ref(false)
const scanning = ref(false)
const importing = ref(false)
const importResult = ref<{ imported: number, skipped: number } | null>(null)

const fileColumns: TableColumn<ScannedFile>[] = [
  {
    accessorKey: 'name',
    header: 'Name',
    meta: { class: { td: 'max-w-[300px]' } }
  },
  { accessorKey: 'type', header: 'Type' },
  {
    accessorKey: 'size',
    header: 'Size',
    cell: ({ row }) => formatSize(row.getValue('size') as number)
  },
  { id: 'actions', header: '' }
]

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function removeFile(index: number) {
  scannedFiles.value.splice(index, 1)
}

function resetModal() {
  folderPath.value = ''
  scannedFiles.value = []
  scanned.value = false
  importResult.value = null
  scanning.value = false
  importing.value = false
}

async function scanFolder() {
  scanning.value = true
  try {
    const res = await $fetch<{ files: ScannedFile[] }>(`${apiBase}/imports/scan`, {
      method: 'POST',
      body: { path: folderPath.value }
    })
    scannedFiles.value = res.files
    scanned.value = true
  }
  catch (err) {
    console.error('Scan failed:', err)
  }
  finally {
    scanning.value = false
  }
}

async function executeImport() {
  importing.value = true
  try {
    const res = await $fetch<{ imported: number, skipped: number }>(`${apiBase}/imports/execute`, {
      method: 'POST',
      body: {
        files: scannedFiles.value.map(f => ({ path: f.path, type: f.type }))
      }
    })
    importResult.value = res
    await refresh()
  }
  catch (err) {
    console.error('Import failed:', err)
  }
  finally {
    importing.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Resources</h1>
      <UButton
        icon="i-lucide-folder-input"
        label="Import Folder"
        @click="resetModal(); importOpen = true"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <NuxtLink v-for="card in cards" :key="card.label" :to="card.to">
        <UCard class="hover:ring-1 hover:ring-primary transition">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon :name="card.icon" class="size-5" />
              <h3 class="font-semibold">{{ card.label }}</h3>
            </div>
          </template>
          <p class="text-3xl font-bold">{{ card.count.value }}</p>
          <p class="text-sm text-muted">items</p>
        </UCard>
      </NuxtLink>
    </div>

    <UModal v-model:open="importOpen" title="Import Folder" :ui="{ width: 'sm:max-w-4xl' }">
      <template #body>
        <!-- Result view -->
        <div v-if="importResult" class="flex flex-col gap-4">
          <p>
            Imported <strong>{{ importResult.imported }}</strong> file(s),
            skipped <strong>{{ importResult.skipped }}</strong> duplicate(s).
          </p>
        </div>

        <!-- Scan + file list view -->
        <div v-else class="flex flex-col gap-4">
          <div class="flex gap-2">
            <UInput
              v-model="folderPath"
              placeholder="/path/to/folder"
              class="flex-1"
              :disabled="scanning"
            />
            <UButton
              label="Scan"
              :loading="scanning"
              :disabled="!folderPath.trim()"
              @click="scanFolder"
            />
          </div>

          <div v-if="scannedFiles.length > 0">
            <UTable :data="scannedFiles" :columns="fileColumns" class="table-fixed">
              <template #name-cell="{ row }">
                <span class="block truncate" :title="row.original.name">{{ row.original.name }}</span>
              </template>
              <template #actions-cell="{ row }">
                <UButton
                  icon="i-lucide-trash-2"
                  variant="ghost"
                  color="error"
                  size="xs"
                  @click="removeFile(scannedFiles.indexOf(row.original))"
                />
              </template>
            </UTable>
          </div>

          <p v-else-if="scanned" class="text-sm text-muted">
            No image or video files found in this folder.
          </p>
        </div>
      </template>

      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Close" variant="outline" @click="close" />
          <UButton
            v-if="!importResult && scannedFiles.length > 0"
            label="Import"
            :loading="importing"
            @click="executeImport"
          />
        </div>
      </template>
    </UModal>
  </div>
</template>
