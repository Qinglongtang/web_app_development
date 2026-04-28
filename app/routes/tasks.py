from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import task as task_model

# 建立任務模組的 Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """
    顯示任務列表。
    支援透過 query string 進行篩選：/?filter=all|pending|completed
    """
    filter_mode = request.args.get('filter', 'all')
    
    # 呼叫 Model 取得對應狀態的任務清單
    tasks = task_model.get_all_tasks(filter_mode)
    
    # 渲染首頁模板並傳入資料
    return render_template('index.html', tasks=tasks, current_filter=filter_mode)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """
    接收新增任務表單。
    """
    content = request.form.get('content')
    
    if not content or not content.strip():
        flash('任務內容不能為空！', 'error')
        return redirect(url_for('tasks.index'))
    
    # 呼叫 Model 實作新增
    if task_model.create_task(content):
        flash('新增任務成功！', 'success')
    else:
        flash('新增任務失敗，請稍後再試。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務狀態。
    """
    if task_model.toggle_task_status(task_id):
        flash('任務狀態已更新！', 'success')
    else:
        flash('更新狀態失敗。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務。
    """
    if task_model.delete_task(task_id):
        flash('任務已成功刪除！', 'success')
    else:
        flash('刪除任務失敗。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """
    編輯任務內容。
    """
    content = request.form.get('content')
    if not content or not content.strip():
        flash('任務內容不能為空！', 'error')
    else:
        if task_model.update_task(task_id, content=content):
            flash('任務已成功更新！', 'success')
        else:
            flash('更新任務失敗。', 'error')
            
    return redirect(url_for('tasks.index'))
