import type { TreeItem } from '@nuxt/ui'
import type { FolderInfo } from '~/types'

export function useFolderTree(folders: Ref<FolderInfo[] | null>) {
  const treeItems = computed<TreeItem[]>(() => {
    const items = folders.value
    if (!items || items.length === 0) return []

    const root: Map<string, { children: Map<string, any>, count: number }> = new Map()

    for (const { folder, count } of items) {
      const parts = folder.split('/').filter(Boolean)
      let current = root
      for (let i = 0; i < parts.length; i++) {
        const part = parts[i]
        if (!current.has(part)) {
          current.set(part, { children: new Map(), count: 0 })
        }
        const node = current.get(part)!
        if (i === parts.length - 1) {
          node.count = count
        }
        current = node.children
      }
    }

    function buildItems(map: Map<string, any>, prefix: string): TreeItem[] {
      const result: TreeItem[] = []
      const sorted = [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]))
      for (const [name, node] of sorted) {
        const path = prefix ? `${prefix}/${name}` : name
        const children = buildItems(node.children, path)
        result.push({
          label: name,
          icon: 'i-lucide-folder',
          defaultExpanded: true,
          value: { path, count: node.count },
          children: children.length > 0 ? children : undefined,
        } as TreeItem)
      }
      return result
    }

    return buildItems(root, '')
  })

  return { treeItems }
}
