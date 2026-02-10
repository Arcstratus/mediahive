<script setup lang="ts">
const open = defineModel<boolean>('open', { default: false })

const emit = defineEmits<{
  imported: []
}>()

const bookmarksApi = useBookmarksApi()
const toast = useToast()

const importText = ref('')
const importFolder = ref('')
const importing = ref(false)

watch(open, (val) => {
  if (!val) return
  importText.value = ''
  importFolder.value = ''
  importing.value = false
})

async function submit() {
  const urls = importText.value.split('\n').map(u => u.trim()).filter(Boolean)
  if (urls.length === 0) return
  importing.value = true
  const items = urls.map(url => ({ title: url, url, folder: importFolder.value || null }))
  const { error } = await bookmarksApi.batchCreate(items)
  importing.value = false
  if (error) { toast.add({ title: error, color: 'error' }); return }
  open.value = false
  emit('imported')
}
</script>

<template>
  <UModal v-model:open="open" title="Import Bookmarks">
    <template #body>
      <div class="flex flex-col gap-4">
        <p class="text-sm text-gray-500">Paste URLs, one per line.</p>
        <UFormField label="Folder" name="importFolder">
          <UInput v-model="importFolder" placeholder="e.g. tech/articles" class="w-full" />
        </UFormField>
        <UTextarea v-model="importText" placeholder="https://example.com&#10;https://another.com" :rows="8" autoresize class="w-full" />
      </div>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Import" :loading="importing" :disabled="!importText.trim()" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
