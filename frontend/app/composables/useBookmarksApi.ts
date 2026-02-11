import type { Bookmark, BookmarkListParams, FolderInfo, PaginatedResponse } from '~/types'

export function useBookmarksApi() {
  const api = useApiFetch()

  return {
    list: (key: string, query?: BookmarkListParams | (() => BookmarkListParams), opts?: { watch?: any[] }) =>
      useAsyncData(key, async () => {
        const q = typeof query === 'function' ? query() : query
        const { data } = await api<PaginatedResponse<Bookmark>>('/bookmarks', { query: q })
        return data
      }, opts),

    create: (body: Record<string, unknown>) =>
      api<Bookmark>('/bookmarks', { method: 'POST', body }),

    batchCreate: (items: Record<string, unknown>[]) =>
      api<{ created: number; items: Bookmark[] }>('/bookmarks/batch', { method: 'POST', body: items }),

    update: (id: number, body: Record<string, unknown>) =>
      api<Bookmark>(`/bookmarks/${id}`, { method: 'PUT', body }),

    remove: (id: number) =>
      api<void>(`/bookmarks/${id}`, { method: 'DELETE' }),

    batchDelete: (ids: number[]) =>
      api<void>('/bookmarks/batch', { method: 'DELETE', body: { ids } }),

    getFolders: (key: string) =>
      useAsyncData(key, async () => {
        const { data } = await api<FolderInfo[]>('/bookmarks/folders')
        return data
      }),
  }
}
