import sqlite3
import os
from flask import current_app

def get_db_connection():
    """
    建立資料庫連線並回傳。
    使用 current_app.config['DATABASE'] 來取得資料庫路徑。
    """
    db_path = current_app.config['DATABASE']
    # 確保目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    初始化資料庫（從 schema.sql 建立資料表）。
    """
    # 取得 schema.sql 的路徑
    # 假設 schema.sql 在根目錄的 database/ 資料夾下
    schema_path = os.path.join(current_app.root_path, '..', 'database', 'schema.sql')
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def create_task(content):
    """
    新增一筆任務。
    """
    if not content or not content.strip():
        return False
        
    conn = None
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (content) VALUES (?)', (content.strip(),))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating task: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_tasks(filter_mode='all'):
    """
    獲取任務清單。
    filter_mode: 'all', 'pending', 'completed'
    """
    conn = None
    try:
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
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_task_by_id(task_id):
    """
    根據 ID 取得單筆任務。
    """
    conn = None
    try:
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return task
    except Exception as e:
        print(f"Error fetching task {task_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_task(task_id, content=None, status=None):
    """
    通用更新任務功能。
    """
    conn = None
    try:
        conn = get_db_connection()
        
        updates = []
        params = []
        
        if content is not None:
            updates.append('content = ?')
            params.append(content.strip())
        
        if status is not None:
            updates.append('status = ?')
            params.append(status)
            
        if not updates:
            return False
            
        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        
        conn.execute(sql, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task {task_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()

def toggle_task_status(task_id):
    """
    切換任務狀態的便捷方法。
    """
    task = get_task_by_id(task_id)
    if task:
        new_status = 'completed' if task['status'] == 'pending' else 'pending'
        return update_task(task_id, status=new_status)
    return False

def delete_task(task_id):
    """
    刪除指定任務。
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()
