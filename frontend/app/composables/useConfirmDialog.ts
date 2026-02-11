import ConfirmDialog from '~/components/ConfirmDialog.vue'

export function useConfirmDialog() {
  const overlay = useOverlay()

  return {
    confirm: async (opts: { title?: string, message: string, confirmLabel?: string, confirmColor?: string }) => {
      const modal = overlay.create(ConfirmDialog)
      const instance = modal.open(opts)
      return await instance.result as boolean
    },
  }
}
