-- 任務管理系統 資料庫 Schema
-- 儲存路徑: database/schema.sql

-- 建立任務資料表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 任務唯一識別碼
    content TEXT NOT NULL,                -- 任務內容
    status TEXT NOT NULL DEFAULT 'pending', -- 任務狀態 (pending: 待辦, completed: 已完成)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- 建立時間
);
