<script setup lang="ts">
interface Tag {
  id: number
  name: string
}

interface Bookmark {
  id: number
  title: string
  url: string
  description: string | null
  folder: string | null
  tags: Tag[]
}

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  bookmark?: Bookmark | null
}>()

const emit = defineEmits<{
  saved: []
}>()

const { public: { apiBase } } = useRuntimeConfig()

const form = reactive({ title: '', url: '', description: '', folder: '', tags: [] as string[] })

const isEditing = computed(() => !!props.bookmark)

watch(open, (val) => {
  if (!val) return
  if (props.bookmark) {
    form.title = props.bookmark.title
    form.url = props.bookmark.url
    form.description = props.bookmark.description ?? ''
    form.folder = props.bookmark.folder ?? ''
    form.tags = props.bookmark.tags.map(t => t.name)
  }
  else {
    form.title = ''
    form.url = ''
    form.description = ''
    form.folder = ''
    form.tags = []
  }
})

async function submit() {
  if (props.bookmark) {
    await $fetch(`${apiBase}/bookmarks/${props.bookmark.id}`, {
      method: 'PUT',
      body: { title: form.title, url: form.url, description: form.description || null, folder: form.folder || null, tags: form.tags }
    })
  }
  else {
    await $fetch(`${apiBase}/bookmarks`, {
      method: 'POST',
      body: { title: form.title, url: form.url, description: form.description || null, folder: form.folder || null, tags: form.tags }
    })
  }
  open.value = false
  emit('saved')
}
</script>

<template>
  <UModal v-model:open="open" :title="isEditing ? 'Edit Bookmark' : 'Add Bookmark'">
    <template #body>
      <div class="flex flex-col gap-4">
        <UFormField label="Title" name="title">
          <UInput v-model="form.title" placeholder="Bookmark title" class="w-full" />
        </UFormField>
        <UFormField label="URL" name="url">
          <UInput v-model="form.url" placeholder="https://example.com" class="w-full" />
        </UFormField>
        <UFormField label="Description" name="description">
          <UTextarea v-model="form.description" placeholder="Description (optional)" class="w-full" />
        </UFormField>
        <UFormField label="Folder" name="folder">
          <UInput v-model="form.folder" placeholder="Folder (optional)" class="w-full" />
        </UFormField>
        <UFormField label="Tags" name="tags">
          <UInputTags v-model="form.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
        </UFormField>
      </div>
    </template>

    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
        <UButton :label="isEditing ? 'Update' : 'Create'" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
