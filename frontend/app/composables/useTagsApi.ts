import type { Tag } from '~/types'

export function useTagsApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    list: (key: string) =>
      useAsyncData(key, () => $fetch<Tag[]>(`${apiBase}/tags`)),

    create: (name: string) =>
      $fetch<Tag>(`${apiBase}/tags`, { method: 'POST', body: { name } }),

    remove: (id: number) =>
      $fetch<void>(`${apiBase}/tags/${id}`, { method: 'DELETE' }),
  }
}
