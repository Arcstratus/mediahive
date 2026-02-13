<script setup lang="ts">
import type { DepartmentTreeNode } from '~/composables/useDemoDepartments'

defineProps<{
  node: DepartmentTreeNode
  depth: number
}>()

const expanded = ref(true)
</script>

<template>
  <div>
    <div
      class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-elevated cursor-pointer"
      :style="{ paddingLeft: `${depth * 24 + 12}px` }"
      @click="expanded = !expanded"
    >
      <UIcon
        v-if="node.children.length > 0"
        :name="expanded ? 'i-lucide-chevron-down' : 'i-lucide-chevron-right'"
        class="size-4 text-muted"
      />
      <span v-else class="size-4" />
      <UIcon name="i-lucide-building" class="size-4 text-primary" />
      <span class="font-medium text-sm">{{ node.department.name }}</span>
      <UBadge :label="`${node.department.memberCount} 人`" variant="subtle" size="xs" />
      <span class="text-xs text-muted ml-auto">{{ node.department.head }}</span>
      <UButton
        icon="i-lucide-pencil"
        variant="ghost"
        color="neutral"
        size="xs"
        :to="`/foundation/department/${node.department.id}`"
        @click.stop
      />
    </div>
    <div v-if="expanded && node.children.length > 0">
      <DepartmentTreeItem
        v-for="child in node.children"
        :key="child.department.id"
        :node="child"
        :depth="depth + 1"
      />
    </div>
  </div>
</template>
