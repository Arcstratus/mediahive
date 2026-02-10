<script setup lang="ts">
import Hls from 'hls.js'

const open = defineModel<boolean>('open', { default: false })

const { public: { apiBase } } = useRuntimeConfig()
const toast = useToast()

const url = ref('')
const error = ref('')
const loading = ref(false)
const downloading = ref(false)
const isPlaying = ref(false)

const videoRef = ref<HTMLVideoElement | null>(null)
let hls: Hls | null = null

function destroyHls() {
  if (hls) {
    hls.destroy()
    hls = null
  }
  isPlaying.value = false
  error.value = ''
}

function loadStream() {
  if (!url.value.trim()) return

  error.value = ''
  loading.value = true
  destroyHls()

  const video = videoRef.value
  if (!video) return

  if (video.canPlayType('application/vnd.apple.mpegurl')) {
    // Native HLS support (Safari)
    video.src = url.value
    video.addEventListener('loadedmetadata', () => {
      loading.value = false
      isPlaying.value = true
      video.play()
    }, { once: true })
    video.addEventListener('error', () => {
      loading.value = false
      error.value = 'Failed to load stream. Please check the URL.'
    }, { once: true })
  } else if (Hls.isSupported()) {
    hls = new Hls()
    hls.loadSource(url.value)
    hls.attachMedia(video)
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      loading.value = false
      isPlaying.value = true
      video.play()
    })
    hls.on(Hls.Events.ERROR, (_event, data) => {
      if (data.fatal) {
        loading.value = false
        error.value = 'Failed to load stream. Please check the URL.'
        destroyHls()
      }
    })
  } else {
    loading.value = false
    error.value = 'Your browser does not support HLS playback.'
  }
}

async function downloadStream() {
  if (!url.value.trim()) return
  downloading.value = true
  try {
    await $fetch(`${apiBase}/resources/download`, {
      method: 'POST',
      body: { url: url.value }
    })
    toast.add({ title: 'Download started', description: 'The stream is being downloaded in the background.', color: 'info' })
  } catch {
    toast.add({ title: 'Download failed', description: 'Failed to start download. Please try again.', color: 'error' })
  } finally {
    downloading.value = false
  }
}

watch(open, (val) => {
  if (!val) {
    destroyHls()
    url.value = ''
    loading.value = false
    downloading.value = false
  }
})
</script>

<template>
  <UModal v-model:open="open" title="Play M3U8 Stream">
    <template #body>
      <div class="flex flex-col gap-4">
        <UFormField label="Stream URL" name="url">
          <div class="flex gap-2">
            <UInput
              v-model="url"
              placeholder="https://example.com/stream.m3u8"
              class="flex-1"
              @keyup.enter="loadStream"
            />
            <UButton label="Load" :loading="loading" :disabled="!url.trim()" @click="loadStream" />
          </div>
        </UFormField>

        <div class="rounded-lg bg-elevated overflow-hidden aspect-video flex items-center justify-center">
          <video
            v-show="isPlaying"
            ref="videoRef"
            controls
            class="w-full h-full"
          />
          <div v-if="!isPlaying && !error" class="text-muted text-sm">
            Enter an M3U8 URL and click Load to start playback
          </div>
        </div>

        <UAlert
          v-if="error"
          :title="error"
          color="error"
          icon="i-lucide-circle-x"
        />
      </div>
    </template>
    <template #footer="{ close }">
      <div class="flex justify-end gap-2">
        <UButton
          label="Download"
          icon="i-lucide-download"
          variant="soft"
          :loading="downloading"
          :disabled="!url.trim()"
          @click="downloadStream"
        />
        <UButton label="Close" variant="outline" color="neutral" @click="close" />
      </div>
    </template>
  </UModal>
</template>
