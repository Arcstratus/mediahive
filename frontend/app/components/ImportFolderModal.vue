<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { ScannedFile, ImportResult } from '~/types'

const open = defineModel<boolean>('open', { default: false })

const emit = defineEmits<{
  imported: [result: ImportResult]
}>()

const { public: { apiBase } } = useRuntimeConfig()

const folderPath = ref('')
const scannedFiles = ref<ScannedFile[]>([])
const scanned = ref(false)
const scanning = ref(false)
const importing = ref(false)
const importResult = ref<ImportResult | null>(null)

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

function reset() {
  folderPath.value = ''
  scannedFiles.value = []
  scanned.value = false
  importResult.value = null
  scanning.value = false
  importing.value = false
}

watch(open, (val) => {
  if (val) reset()
})

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
    const res = await $fetch<ImportResult>(`${apiBase}/imports/execute`, {
      method: 'POST',
      body: {
        files: scannedFiles.value.map(f => ({ path: f.path, type: f.type }))
      }
    })
    importResult.value = res
    emit('imported', res)
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
  <UModal v-model:open="open" title="Import Folder" :ui="{ width: 'sm:max-w-4xl' }">
    <template #body>
      <div v-if="importResult" class="flex flex-col gap-4">
        <p>
          Imported <strong>{{ importResult.imported }}</strong> file(s),
          skipped <strong>{{ importResult.skipped }}</strong> duplicate(s).
        </p>
      </div>

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
</template>
