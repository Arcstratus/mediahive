import type { Stats } from '~/types'

export function useStatsApi() {
  const { public: { apiBase } } = useRuntimeConfig()

  return {
    get: (key: string) =>
      useAsyncData(key, () => $fetch<Stats>(`${apiBase}/stats`)),
  }
}
