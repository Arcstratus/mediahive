# MediaHive TODO

## Frontend

### Code Duplication

- [ ] `buildTree()` 在 `resources/index.vue` 和 `bookmarks.vue` 中完全重複，應抽至共用 composable
- [ ] `resources/viewer.vue` 和 `folders/viewer.vue` 大量重複（cache、preload、keyboard navigation、form），應抽至 `useResourceViewer` composable
- [ ] filter query 建構邏輯在 resources 和 bookmarks 頁面相似，可抽象化

### Types

- [ ] `ApiResult<T>` 僅定義在 `useApiFetch.ts`，應移至 `types/index.ts`
- [ ] Filter / pagination 參數用 `Record<string, unknown>`，應定義具體 interface
- [ ] `ViewMode` type `'list' | 'tree'` 重複出現，應抽為 type alias

### UI/UX

- [ ] 刪除確認使用瀏覽器 `confirm()`，應改用 Modal 元件
- [ ] `TestCard.vue` 似乎未使用，應移除
- [ ] Tree view 未支援鍵盤導航
- [ ] 操作按鈕（edit/delete）僅在 hover 時顯示（`opacity-0`），觸控裝置無法操作且 screen reader 不可見

### SSR / Hydration

- [ ] 含 client-side 動態狀態的元件（如 `selectedCount`、`rowSelection`）可能造成 hydration mismatch
- [ ] 刪除按鈕 `color="error"` 有時 SSR 先渲染為預設色再跳為紅色，應用 `<ClientOnly>` 包裹操作列

### Form Validation

- [ ] BookmarkModal 無 URL 格式驗證
- [ ] EditResourceModal 無輸入驗證
- [ ] ImportBookmarksModal 無格式驗證

---

## Feature Ideas

### 整理與歸檔

- [ ] 批次加 tag — 勾選多個資源後一次加上相同標籤
- [ ] 批次移動資料夾 — 勾選後移到指定 folder
- [ ] 拖曳排序 / 拖曳到資料夾 — 在 tree view 裡直接拖
- [ ] 書籤資料夾瀏覽頁 — 書籤有 folder 欄位但沒有像 resources 那樣的 folder 瀏覽頁

### 搜尋與篩選

- [ ] 全域搜尋 — 一個搜尋框同時搜 resources + bookmarks，從 Dashboard 直接用
- [ ] 日期範圍篩選 — 找「上個月加入的」資源
- [ ] 依檔案大小排序/篩選 — 找大檔案清理空間
- [ ] Tag 交集/聯集切換 — 目前多 tag 篩選是交集，有時需要聯集

### 匯入與匯出

- [ ] 瀏覽器書籤匯入 — 支援標準 HTML 書籤格式（Chrome/Firefox 匯出的）
- [ ] 匯出書籤 — 匯出為 HTML 或 JSON，方便備份或遷移
- [ ] 匯出資源清單 — CSV/JSON 匯出 metadata

### 媒體瀏覽

- [ ] 圖片 gallery / slideshow 模式 — 自動播放瀏覽
- [ ] 影片播放清單 — 連續播放多個影片
- [ ] 資源預覽放大 — 在列表頁 hover 或點擊可快速預覽，不用進 viewer

### 資料管理

- [ ] 重複偵測 — 上傳或匯入時提示已存在相同檔案
- [ ] 儲存空間統計 — Dashboard 顯示總使用量、各類型佔比
- [ ] 未分類提醒 — 顯示沒有 tag、沒有 folder 的資源數量，引導整理
- [ ] 資源收藏 / 我的最愛功能

### 頁面佈局調整

- [ ] Resources 清單頁只保留 table view，移除 tree view
- [ ] Bookmarks 清單頁只保留 table view，移除 tree view
- [ ] Tree view 移至 Folders 頁面（資源的資料夾瀏覽以 tree 呈現）
