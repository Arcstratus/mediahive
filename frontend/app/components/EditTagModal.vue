<script setup lang="ts">
import type { Tag } from '~/types'

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  tag: Tag | null
}>()

const emit = defineEmits<{
  updated: []
}>()

const tagsApi = useTagsApi()
const toast = useToast()

const tagName = ref('')

watch(open, (val) => {
  if (!val) return
  tagName.value = props.tag?.name ?? ''
})

async function submit() {
  if (!tagName.value.trim() || !props.tag) return
  const { error } = await tagsApi.update(props.tag.id, tagName.value.trim())
  if (error) { toast.add({ title: error, color: 'error' }); return }
  open.value = false
  emit('updated')
}
</script>

<template>
  <UModal v-model:open="open" title="Edit Tag">
    <template #body>
      <UFormField label="Name" name="name">
        <UInput v-model="tagName" placeholder="Tag name" class="w-full" @keyup.enter="submit" />
      </UFormField>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Save" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
