<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'

definePageMeta({
  layout: 'dashboard'
})

interface Tag {
  id: number
  name: string
  created_at: string
}

interface Resource {
  id: number
  type: string
  url: string | null
  title: string | null
  folder: string | null
  tags: Tag[]
  created_at: string
}

interface PaginatedResponse {
  items: Resource[]
  total: number
  page: number
  per_page: number
}

const VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.ts']

const { public: { apiBase } } = useRuntimeConfig()

const page = ref(1)
const perPage = 20
const filterSearch = ref('')
const filterTags = ref<string[]>([])
const filterExt = ref<string[]>([])
const sorting = ref<{ id: string, desc: boolean }[]>([])

const extOptions = computed(() =>
  VIDEO_EXTENSIONS.map(e => ({ label: e, value: e }))
)

const { data: allTags, refresh: refreshTags } = await useAsyncData<Tag[]>('video-tags', () =>
  $fetch(`${apiBase}/tags`)
)

const tagFilterOptions = computed(() =>
  (allTags.value ?? []).map(t => ({ label: t.name, value: t.name }))
)

const { data, refresh } = await useAsyncData<PaginatedResponse>(
  'video-resources',
  () => {
    const query: Record<string, unknown> = {
      type: 'video',
      page: page.value,
      per_page: perPage
    }
    if (filterSearch.value) query.search = filterSearch.value
    if (filterTags.value.length) query.tag = filterTags.value
    if (filterExt.value.length) query.ext = filterExt.value
    if (sorting.value.length) {
      query.sort_by = sorting.value[0].id
      query.sort_desc = sorting.value[0].desc
    }
    return $fetch(`${apiBase}/resources`, { query })
  },
  { watch: [filterSearch, filterTags, filterExt, page, sorting] }
)

const resources = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)

watch([filterSearch, filterTags, filterExt], () => {
  page.value = 1
})

function getExtension(url: string | null): string {
  if (!url) return ''
  const dot = url.lastIndexOf('.')
  return dot >= 0 ? url.slice(dot) : ''
}

function sortHeader(label: string) {
  return ({ column }: { column: { getIsSorted: () => false | 'asc' | 'desc', toggleSorting: (asc: boolean) => void } }) => {
    const isSorted = column.getIsSorted()
    return h(resolveComponent('UButton'), {
      color: 'neutral',
      variant: 'ghost',
      label,
      icon: isSorted
        ? (isSorted === 'asc' ? 'i-lucide-arrow-up-narrow-wide' : 'i-lucide-arrow-down-wide-narrow')
        : 'i-lucide-arrow-up-down',
      class: '-mx-2.5',
      onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
    })
  }
}

const rowSelection = ref<Record<string, boolean>>({})

const selectedCount = computed(() => Object.values(rowSelection.value).filter(Boolean).length)

async function batchDelete() {
  if (!confirm(`Are you sure you want to delete ${selectedCount.value} selected video(s)?`)) return
  const ids = Object.keys(rowSelection.value).filter(k => rowSelection.value[k]).map(Number)
  await $fetch(`${apiBase}/resources/batch-delete`, {
    method: 'POST',
    body: { ids }
  })
  rowSelection.value = {}
  await refresh()
}

const UCheckbox = resolveComponent('UCheckbox')

const columns: TableColumn<Resource>[] = [
  {
    id: 'select',
    header: ({ table }) => h(UCheckbox, {
      'modelValue': table.getIsSomePageRowsSelected() ? 'indeterminate' : table.getIsAllPageRowsSelected(),
      'onUpdate:modelValue': (value: boolean) => table.toggleAllPageRowsSelected(!!value),
      'aria-label': 'Select all'
    }),
    cell: ({ row }) => h(UCheckbox, {
      'modelValue': row.getIsSelected(),
      'onUpdate:modelValue': (value: boolean) => row.toggleSelected(!!value),
      'aria-label': 'Select row'
    })
  },
  { accessorKey: 'title', header: sortHeader('Title'), maxSize: 300 },
  { id: 'ext', accessorFn: row => getExtension(row.url), header: sortHeader('Extension') },
  { id: 'tags', header: 'Tags' },
  { accessorKey: 'created_at', header: sortHeader('Created At') },
  { id: 'actions', header: '' }
]

// Edit modal
const modalOpen = ref(false)
const editingResource = ref<Resource | null>(null)
const form = reactive({ title: '', folder: '', tags: [] as string[] })

function openEdit(resource: Resource) {
  editingResource.value = resource
  form.title = resource.title ?? ''
  form.folder = resource.folder ?? ''
  form.tags = resource.tags.map(t => t.name)
  modalOpen.value = true
}

async function submitForm() {
  if (!editingResource.value) return
  await $fetch(`${apiBase}/resources/${editingResource.value.id}`, {
    method: 'PUT',
    body: { title: form.title, folder: form.folder || null, tags: form.tags }
  })
  modalOpen.value = false
  await refresh()
  await refreshTags()
}

async function deleteResource(id: number) {
  if (!confirm('Are you sure you want to delete this video?')) return
  await $fetch(`${apiBase}/resources/${id}`, { method: 'DELETE' })
  await refresh()
}

async function removeTag(resource: Resource, tagName: string) {
  const updatedTags = resource.tags.filter(t => t.name !== tagName).map(t => t.name)
  await $fetch(`${apiBase}/resources/${resource.id}`, {
    method: 'PUT',
    body: { tags: updatedTags }
  })
  await refresh()
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

// Upload modal
const uploadOpen = ref(false)
const uploadFile = ref<File | null>(null)
const uploadForm = reactive({ title: '', tags: [] as string[] })
const uploading = ref(false)

function openUpload() {
  uploadFile.value = null
  uploadForm.title = ''
  uploadForm.tags = []
  uploading.value = false
  uploadOpen.value = true
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  uploadFile.value = input.files?.[0] ?? null
}

async function submitUpload() {
  if (!uploadFile.value) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    if (uploadForm.title) formData.append('title', uploadForm.title)
    if (uploadForm.tags.length) formData.append('tags', uploadForm.tags.join(','))
    await $fetch(`${apiBase}/resources/upload`, {
      method: 'POST',
      body: formData
    })
    uploadOpen.value = false
    await refresh()
    await refreshTags()
  }
  finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <UBreadcrumb
      :items="[
        { label: 'Resources', to: '/resources' },
        { label: 'Videos' }
      ]"
    />

    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Video Resources</h1>
      <UButton label="Add Video" icon="i-lucide-plus" @click="openUpload" />
    </div>

    <div class="flex items-center gap-2">
      <UInput
        v-model="filterSearch"
        placeholder="Search title..."
        icon="i-lucide-search"
        class="w-64"
      />
      <USelectMenu
        v-model="filterExt"
        :items="extOptions"
        value-key="value"
        placeholder="Extension"
        multiple
        class="w-48"
      />
      <USelectMenu
        v-model="filterTags"
        :items="tagFilterOptions"
        value-key="value"
        placeholder="Filter by tags"
        multiple
        class="w-64"
      />
    </div>

    <div class="flex items-center gap-2">
      <UButton
        :label="selectedCount > 0 ? `Delete Selected (${selectedCount})` : 'Delete Selected'"
        icon="i-lucide-trash-2"
        color="error"
        variant="soft"
        :disabled="selectedCount === 0"
        @click="batchDelete"
      />
    </div>

    <UTable v-model:sorting="sorting" v-model:row-selection="rowSelection" :data="resources" :columns="columns" :sorting-options="{ manualSorting: true }" :get-row-id="(row: Resource) => String(row.id)">
      <template #title-cell="{ row }">
        <span class="block max-w-xs truncate" :title="row.original.title ?? ''">{{ row.original.title }}</span>
      </template>

      <template #ext-cell="{ row }">
        <UBadge :label="getExtension(row.original.url)" variant="subtle" size="sm" />
      </template>

      <template #tags-cell="{ row }">
        <div class="flex gap-1 flex-wrap">
          <UBadge
            v-for="tag in row.original.tags"
            :key="tag.id"
            :label="tag.name"
            variant="subtle"
            size="sm"
            trailing-icon="i-lucide-x"
            class="cursor-pointer"
            @click="removeTag(row.original, tag.name)"
          />
        </div>
      </template>

      <template #created_at-cell="{ row }">
        {{ formatDate(row.original.created_at) }}
      </template>

      <template #actions-cell="{ row }">
        <div class="flex gap-1 justify-end">
          <UButton
            icon="i-lucide-eye"
            variant="ghost"
            color="neutral"
            size="xs"
            :to="`/resources/videos/viewer?id=${row.original.id}`"
          />
          <UButton
            icon="i-lucide-pencil"
            variant="ghost"
            color="neutral"
            size="xs"
            @click="openEdit(row.original)"
          />
          <UButton
            icon="i-lucide-trash-2"
            variant="ghost"
            color="error"
            size="xs"
            @click="deleteResource(row.original.id)"
          />
        </div>
      </template>
    </UTable>

    <div v-if="total > perPage" class="flex justify-center">
      <UPagination v-model:page="page" :total="total" :items-per-page="perPage" />
    </div>

    <!-- Edit modal -->
    <UModal v-model:open="modalOpen" title="Edit Video">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="Title" name="title">
            <UInput v-model="form.title" placeholder="Video title" class="w-full" />
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
          <UButton label="Update" @click="submitForm" />
        </div>
      </template>
    </UModal>

    <!-- Upload modal -->
    <UModal v-model:open="uploadOpen" title="Upload Video">
      <template #body>
        <div class="flex flex-col gap-4">
          <UFormField label="File" name="file">
            <input type="file" accept="video/*" @change="onFileChange">
          </UFormField>
          <UFormField label="Title" name="title">
            <UInput v-model="uploadForm.title" placeholder="Video title (optional)" class="w-full" />
          </UFormField>
          <UFormField label="Tags" name="tags">
            <UInputTags v-model="uploadForm.tags" placeholder="Add tags..." :add-on-blur="true" class="w-full" />
          </UFormField>
        </div>
      </template>
      <template #footer="{ close }">
        <div class="flex justify-end gap-2">
          <UButton label="Cancel" variant="outline" color="neutral" @click="close" />
          <UButton label="Upload" :loading="uploading" :disabled="!uploadFile" @click="submitUpload" />
        </div>
      </template>
    </UModal>
  </div>
</template>
