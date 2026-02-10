import type { Stats } from '~/types'

export function useStatsApi() {
  const api = useApiFetch()

  return {
    get: (key: string) =>
      useAsyncData(key, async () => {
        const { data } = await api<Stats>('/stats')
        return data
      }),
  }
}
