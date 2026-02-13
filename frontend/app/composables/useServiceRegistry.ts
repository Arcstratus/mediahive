import type { ServiceConfig, SidebarItem } from '~/services/registry'
import type { DomainConfig } from '~/services/domains'
import { allServices } from '~/services/registry'
import { allDomains, serviceToDomain } from '~/services/domains'

export function useServiceRegistry() {
  const route = useRoute()

  /** 從路由路徑比對當前服務（長路徑優先匹配） */
  const currentService = computed<ServiceConfig | undefined>(() => {
    const path = route.path
    // 以路徑長度排序（長路徑優先），避免 /resources 匹配到 /re 等短路徑
    const sorted = [...allServices].sort((a, b) => b.path.length - a.path.length)
    return sorted.find(s => path === s.path || path.startsWith(s.path + '/'))
  })

  /** 當前服務所屬領域 */
  const currentDomain = computed<DomainConfig | undefined>(() => {
    const service = currentService.value
    if (!service) return undefined
    return serviceToDomain[service.id]
  })

  /** 當前領域的所有服務產生的 sidebar 項目 */
  const sidebarItems = computed<SidebarItem[]>(() => {
    const domain = currentDomain.value
    if (!domain) return []

    return domain.services.map((service) => {
      if (service.sidebar.length > 0) {
        return {
          label: service.label,
          icon: service.icon,
          defaultOpen: true,
          children: service.sidebar,
        }
      }
      return {
        label: service.label,
        icon: service.icon,
        to: service.path,
      }
    })
  })

  /** Navbar 領域下拉選單選項（選擇後導航到該領域第一個服務） */
  const domainMenuItems = computed(() => [
    allDomains.map(domain => ({
      label: domain.label,
      icon: domain.icon,
      onSelect() {
        const firstService = domain.services[0]
        if (firstService) {
          navigateTo(firstService.path)
        }
      },
    })),
  ])

  return {
    currentService,
    currentDomain,
    sidebarItems,
    domainMenuItems,
  }
}
