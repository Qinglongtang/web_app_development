import sqlite3
import os

# 資料庫檔案路徑，存放在專案根目錄的 instance 資料夾下
# 註：在實際 Flask 運作時，建議由外部傳入路徑或從 app.config 讀取
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立資料庫連線並回傳"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳結果可以像字典一樣存取 (例如 row['content'])
    return conn

def init_db():
    """初始化資料庫（執行 schema.sql）"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn = get_db_connection()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

def create_task(content):
    """新增一筆任務"""
    if not content.strip():
        return False
        
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return True

def get_all_tasks(filter_mode='all'):
    """
    獲取任務清單
    filter_mode: 'all', 'pending', 'completed'
    """
    conn = get_db_connection()
    query = 'SELECT * FROM tasks'
    params = ()

    if filter_mode == 'pending':
        query += ' WHERE status = ?'
        params = ('pending',)
    elif filter_mode == 'completed':
        query += ' WHERE status = ?'
        params = ('completed',)
    
    query += ' ORDER BY created_at DESC'
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    return tasks

def toggle_task_status(task_id):
    """
    切換任務狀態 (pending -> completed / completed -> pending)
    """
    conn = get_db_connection()
    task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task:
        new_status = 'completed' if task['status'] == 'pending' else 'pending'
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
    
    conn.close()

def delete_task(task_id):
    """刪除指定任務"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
