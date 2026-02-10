import type { ScannedFile, ImportResult } from '~/types'

export function useImportsApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    scan: (path: string) =>
      $fetch<{ files: ScannedFile[] }>(`${apiBase}/imports/scan`, { method: 'POST', body: { path } }),

    execute: (files: { path: string; type: string }[]) =>
      $fetch<ImportResult>(`${apiBase}/imports/execute`, { method: 'POST', body: { files } }),
  }
}
