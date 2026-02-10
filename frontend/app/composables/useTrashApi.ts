import type { TrashItem } from '~/types'

export function useTrashApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    list: (key: string) =>
      useAsyncData(key, () => $fetch<TrashItem[]>(`${apiBase}/trash`)),

    restore: (id: number) =>
      $fetch<void>(`${apiBase}/trash/${id}/restore`, { method: 'POST' }),

    remove: (id: number) =>
      $fetch<void>(`${apiBase}/trash/${id}`, { method: 'DELETE' }),

    empty: () =>
      $fetch<void>(`${apiBase}/trash`, { method: 'DELETE' }),
  }
}
