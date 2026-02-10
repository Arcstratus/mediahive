import type { Resource, PaginatedResponse, FolderInfo } from '~/types'

export function useResourcesApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    list: (key: string, query?: Record<string, unknown> | (() => Record<string, unknown>), opts?: { watch?: any[] }) =>
      useAsyncData(key, () => {
        const q = typeof query === 'function' ? query() : query
        return $fetch<PaginatedResponse<Resource>>(`${apiBase}/resources`, { query: q })
      }, opts),

    get: (id: number) =>
      $fetch<Resource>(`${apiBase}/resources/${id}`),

    getIds: (params?: Record<string, unknown>) =>
      $fetch<number[]>(`${apiBase}/resources/ids`, { params }),

    update: (id: number, body: Record<string, unknown>) =>
      $fetch<Resource>(`${apiBase}/resources/${id}`, { method: 'PUT', body }),

    remove: (id: number) =>
      $fetch<void>(`${apiBase}/resources/${id}`, { method: 'DELETE' }),

    batchDelete: (ids: number[]) =>
      $fetch<void>(`${apiBase}/resources/batch-delete`, { method: 'POST', body: { ids } }),

    upload: (body: FormData) =>
      $fetch<void>(`${apiBase}/resources/upload`, { method: 'POST', body }),

    download: (url: string) =>
      $fetch<void>(`${apiBase}/resources/download`, { method: 'POST', body: { url } }),

    getFolders: (key: string) =>
      useAsyncData(key, () => $fetch<FolderInfo[]>(`${apiBase}/resources/folders`)),

    setThumbnail: (id: number, timestamp: number) =>
      $fetch<Resource>(`${apiBase}/resources/${id}/thumbnail`, { method: 'POST', body: { timestamp } }),

    removeThumbnail: (id: number) =>
      $fetch<Resource>(`${apiBase}/resources/${id}/thumbnail`, { method: 'DELETE' }),
  }
}
