import type { Resource, ResourceListParams, ResourceIdParams, PaginatedResponse, FolderInfo } from '~/types'

export function useResourcesApi() {
  const api = useApiFetch()

  return {
    list: (key: string, query?: ResourceListParams | (() => ResourceListParams), opts?: { watch?: any[] }) =>
      useAsyncData(key, async () => {
        const q = typeof query === 'function' ? query() : query
        const { data } = await api<PaginatedResponse<Resource>>('/resources', { query: q })
        return data
      }, opts),

    get: (id: number) =>
      api<Resource>(`/resources/${id}`),

    getIds: (params?: ResourceIdParams) =>
      api<number[]>('/resources/ids', { params }),

    update: (id: number, body: Record<string, unknown>) =>
      api<Resource>(`/resources/${id}`, { method: 'PUT', body }),

    remove: (id: number) =>
      api<void>(`/resources/${id}`, { method: 'DELETE' }),

    batchDelete: (ids: number[]) =>
      api<void>('/resources/batch-delete', { method: 'POST', body: { ids } }),

    upload: (body: FormData) =>
      api<void>('/resources/upload', { method: 'POST', body }),

    download: (url: string) =>
      api<void>('/resources/download', { method: 'POST', body: { url } }),

    getFolders: (key: string) =>
      useAsyncData(key, async () => {
        const { data } = await api<FolderInfo[]>('/resources/folders')
        return data
      }),

    setThumbnail: (id: number, timestamp: number) =>
      api<Resource>(`/resources/${id}/thumbnail`, { method: 'POST', body: { timestamp } }),

    removeThumbnail: (id: number) =>
      api<Resource>(`/resources/${id}/thumbnail`, { method: 'DELETE' }),
  }
}
