import type { FetchOptions } from 'ofetch'

type ApiResult<T> = { data: T; error: null } | { data: null; error: string }

export function useApiFetch() {
  const { public: { apiBase } } = useRuntimeConfig()

  return async <T>(url: string, opts?: FetchOptions): Promise<ApiResult<T>> => {
    try {
      const data = await $fetch<T>(`${apiBase}${url}`, opts as any)
      return { data, error: null }
    }
    catch (e: any) {
      const msg = e?.data?.error ?? e?.data?.detail
      return { data: null, error: msg ? String(msg) : 'An error occurred' }
    }
  }
}
