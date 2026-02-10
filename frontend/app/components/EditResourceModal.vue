<script setup lang="ts">
import type { Resource } from '~/types'

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  resource?: Resource | null
}>()

const emit = defineEmits<{
  saved: []
}>()

const resourcesApi = useResourcesApi()
const toast = useToast()

const form = reactive({ title: '', folder: '', tags: [] as string[] })

watch(open, (val) => {
  if (!val) return
  if (props.resource) {
    form.title = props.resource.title ?? ''
    form.folder = props.resource.folder ?? ''
    form.tags = props.resource.tags.map(t => t.name)
  }
})

async function submit() {
  if (!props.resource) return
  const { error } = await resourcesApi.update(props.resource.id, { title: form.title, folder: form.folder || null, tags: form.tags })
  if (error) { toast.add({ title: error, color: 'error' }); return }
  open.value = false
  emit('saved')
}
</script>

<template>
  <UModal v-model:open="open" title="Edit Resource">
    <template #body>
      <div class="flex flex-col gap-4">
        <UFormField label="Title" name="title">
          <UInput v-model="form.title" placeholder="Resource title" class="w-full" />
        </UFormField>
        <UFormField label="Folder" name="folder">
          <UInput v-model="form.folder" placeholder="e.g. 2024/vacation" class="w-full" />
        </UFormField>
        <UFormField label="Tags" name="tags">
          <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
        </UFormField>
      </div>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Update" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
