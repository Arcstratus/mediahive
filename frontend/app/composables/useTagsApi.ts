import type { Tag } from '~/types'

export function useTagsApi() {
  const api = useApiFetch()

  return {
    list: (key: string) =>
      useAsyncData(key, async () => {
        const { data } = await api<Tag[]>('/tags')
        return data
      }),

    create: (name: string) =>
      api<Tag>('/tags', { method: 'POST', body: { name } }),

    update: (id: number, name: string) =>
      api<Tag>(`/tags/${id}`, { method: 'PATCH', body: { name } }),

    remove: (id: number) =>
      api<void>(`/tags/${id}`, { method: 'DELETE' }),
  }
}
