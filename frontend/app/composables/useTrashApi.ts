import type { TrashItem } from '~/types'

export function useTrashApi() {
  const api = useApiFetch()

  return {
    list: (key: string) =>
      useAsyncData(key, async () => {
        const { data } = await api<TrashItem[]>('/trash')
        return data
      }),

    restore: (id: number) =>
      api<void>(`/trash/${id}/restore`, { method: 'POST' }),

    remove: (id: number) =>
      api<void>(`/trash/${id}`, { method: 'DELETE' }),

    empty: () =>
      api<void>('/trash', { method: 'DELETE' }),
  }
}
