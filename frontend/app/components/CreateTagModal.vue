<script setup lang="ts">
const open = defineModel<boolean>('open', { default: false })

const emit = defineEmits<{
  created: []
}>()

const tagsApi = useTagsApi()
const toast = useToast()

const tagName = ref('')

watch(open, (val) => {
  if (!val) return
  tagName.value = ''
})

async function submit() {
  if (!tagName.value.trim()) return
  const { error } = await tagsApi.create(tagName.value.trim())
  if (error) { toast.add({ title: error, color: 'error' }); return }
  open.value = false
  emit('created')
}
</script>

<template>
  <UModal v-model:open="open" title="Add Tag">
    <template #body>
      <UFormField label="Name" name="name">
        <UInput v-model="tagName" placeholder="Tag name" class="w-full" @keyup.enter="submit" />
      </UFormField>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton label="Create" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
