<script setup lang="ts">
const open = defineModel<boolean>('open', { default: false })

const emit = defineEmits<{
  downloaded: []
}>()

const resourcesApi = useResourcesApi()
const toast = useToast()

const url = ref('')
const downloading = ref(false)

watch(open, (val) => {
  if (!val) return
  url.value = ''
  downloading.value = false
})

async function submit() {
  if (!url.value) return
  downloading.value = true
  try {
    await resourcesApi.download(url.value)
    open.value = false
    toast.add({ title: 'Download started', description: 'The file is being downloaded in the background.', color: 'info' })
    emit('downloaded')
  }
  finally {
    downloading.value = false
  }
}
</script>

<template>
  <UModal v-model:open="open" title="Download from URL">
    <template #body>
      <UFormField label="URL" name="url">
        <UInput v-model="url" placeholder="https://example.com/file.mp4" class="w-full" />
      </UFormField>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Download" :loading="downloading" :disabled="!url" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
