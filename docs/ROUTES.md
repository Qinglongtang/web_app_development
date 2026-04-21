# 路由設計文件 (ROUTES.md) - 任務管理系統

## 1. 路由總覽表格

本系統使用 Flask Blueprint `tasks_bp` 來管理任務相關路由。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (任務清單)** | `GET` | `/` | `index.html` | 顯示任務清單。支援 Query String `filter` (all, pending, completed)。 |
| **新增任務** | `POST` | `/add` | — (Redirect) | 接收表單 `content` 欄位，呼叫 Model 新增任務後重新導向回 `/`。 |
| **切換狀態** | `POST` | `/toggle/<int:id>` | — (Redirect) | 切換指定 ID 任務的狀態後重新導向回 `/`。 |
| **刪除任務** | `POST` | `/delete/<int:id>` | — (Redirect) | 刪除指定 ID 任務後重新導向回 `/`。 |

---

## 2. 路由詳細說明

### `GET /` - 任務列表
- **輸入**：URL 參數 `filter` (選填，預設為 `all`)。
- **處理邏輯**：
  1. 從 URL 讀取 `filter` 參數。
  2. 呼叫 `task_model.get_all_tasks(filter_mode)`。
  3. 將結果傳入模板進行渲染。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：若資料庫連線失敗，回傳伺服器錯誤提示。

### `POST /add` - 新增任務
- **輸入**：表單欄位 `content` (String, 必填)。
- **處理邏輯**：
  1. 從 `request.form` 取得 `content`。
  2. 若內容為空，跳回首頁並顯示提示。
  3. 呼叫 `task_model.create_task(content)`。
- **輸出**：`redirect(url_for('tasks.index'))`。

### `POST /toggle/<int:id>` - 更新狀態
- **輸入**：路徑參數 `id` (Integer)。
- **處理邏輯**：隨即呼叫 `task_model.toggle_task_status(id)`。
- **輸出**：`redirect(url_for('tasks.index'))`。

### `POST /delete/<int:id>` - 刪除任務
- **輸入**：路徑參數 `id` (Integer)。
- **處理邏輯**：呼叫 `task_model.delete_task(id)`。
- **輸出**：`redirect(url_for('tasks.index'))`。

---

## 3. Jinja2 模板清單

所有的模板將存放在 `app/templates/` 目錄。

1. **`base.html`**：基礎佈局模板，包含導覽列、頁首、頁尾與 CSS 引用。
2. **`index.html`**：主頁面，繼承 `base.html`。
   - 包含新增任務的表單。
   - 包含任務清單的列表循環 (`for task in tasks`)。
   - 包含篩選器連結路徑。

---

## 4. 路由骨架程式碼

實作於 `app/routes/tasks.py`，定義了 Blueprint 與對應的裝飾器。

### 設計決策
- **Blueprint 命名**：使用 `tasks` 作為 Blueprint 點綴，這意味著在代碼中應使用 `url_for('tasks.index')` 進行跳轉。
- **PRG 模式**：所有 POST 操作 (Add, Toggle, Delete) 後皆採取重導向，確保瀏覽器行為穩定。

---
