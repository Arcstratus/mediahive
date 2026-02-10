import type { ScannedFile, ImportResult } from '~/types'

export function useImportsApi() {
  const api = useApiFetch()

  return {
    scan: (path: string) =>
      api<{ files: ScannedFile[] }>('/imports/scan', { method: 'POST', body: { path } }),

    execute: (files: { path: string; type: string }[]) =>
      api<ImportResult>('/imports/execute', { method: 'POST', body: { files } }),
  }
}
