import type { Bookmark, PaginatedResponse } from '~/types'

export function useBookmarksApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    list: (key: string, query?: Record<string, unknown> | (() => Record<string, unknown>), opts?: { watch?: any[] }) =>
      useAsyncData(key, () => {
        const q = typeof query === 'function' ? query() : query
        return $fetch<PaginatedResponse<Bookmark>>(`${apiBase}/bookmarks`, { query: q })
      }, opts),

    create: (body: Record<string, unknown>) =>
      $fetch<Bookmark>(`${apiBase}/bookmarks`, { method: 'POST', body }),

    update: (id: number, body: Record<string, unknown>) =>
      $fetch<Bookmark>(`${apiBase}/bookmarks/${id}`, { method: 'PUT', body }),

    remove: (id: number) =>
      $fetch<void>(`${apiBase}/bookmarks/${id}`, { method: 'DELETE' }),

    batchDelete: (ids: number[]) =>
      $fetch<void>(`${apiBase}/bookmarks/batch-delete`, { method: 'POST', body: { ids } }),
  }
}
