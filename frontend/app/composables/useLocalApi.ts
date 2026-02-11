import type { ScannedFile, ImportResult } from '~/types'

export function useLocalApi() {
  const api = useApiFetch()

  return {
    scan: (path: string) =>
      api<{ files: ScannedFile[] }>('/local/scan', { method: 'POST', body: { path } }),

    import: (files: { path: string; type: string }[]) =>
      api<ImportResult>('/local/import', { method: 'POST', body: { files } }),
  }
}
