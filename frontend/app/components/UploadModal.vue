<script setup lang="ts">
const open = defineModel<boolean>('open', { default: false })

const emit = defineEmits<{
  uploaded: []
}>()

const resourcesApi = useResourcesApi()
const toast = useToast()

const file = ref<File | null>(null)
const form = reactive({ title: '', tags: [] as string[] })
const uploading = ref(false)

watch(open, (val) => {
  if (!val) return
  file.value = null
  form.title = ''
  form.tags = []
  uploading.value = false
})

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  file.value = input.files?.[0] ?? null
}

async function submit() {
  if (!file.value) return
  uploading.value = true
  const formData = new FormData()
  formData.append('file', file.value)
  if (form.title) formData.append('title', form.title)
  if (form.tags.length) formData.append('tags', form.tags.join(','))
  const { error } = await resourcesApi.upload(formData)
  uploading.value = false
  if (error) { toast.add({ title: error, color: 'error' }); return }
  open.value = false
  emit('uploaded')
}
</script>

<template>
  <UModal v-model:open="open" title="Upload File">
    <template #body>
      <div class="flex flex-col gap-4">
        <UFormField label="File" name="file">
          <input type="file" accept="image/*,video/*" @change="onFileChange">
        </UFormField>
        <UFormField label="Title" name="title">
          <UInput v-model="form.title" placeholder="Title (optional)" class="w-full" />
        </UFormField>
        <UFormField label="Tags" name="tags">
          <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
        </UFormField>
      </div>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Upload" :loading="uploading" :disabled="!file" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
