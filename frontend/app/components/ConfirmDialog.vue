<script setup lang="ts">
const props = defineProps<{
  title?: string
  message: string
  confirmLabel?: string
  confirmColor?: string
}>()

const emit = defineEmits<{
  close: [confirmed: boolean]
}>()
</script>

<template>
  <UModal :title="props.title ?? 'Confirm'" @update:open="(val) => { if (!val) emit('close', false) }">
    <template #body>
      <p>{{ props.message }}</p>
    </template>
    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton label="Cancel" variant="outline" color="neutral" @click="emit('close', false)" />
        <UButton :label="props.confirmLabel ?? 'Confirm'" :color="(props.confirmColor as any) ?? 'error'" @click="emit('close', true)" />
      </div>
    </template>
  </UModal>
</template>
