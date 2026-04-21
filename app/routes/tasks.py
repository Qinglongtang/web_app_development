from flask import Blueprint, render_template, request, redirect, url_for
# 注意：在實作階段會引入 app.models.task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """
    顯示任務列表。
    支援透過 query string 進行篩選：/?filter=all|pending|completed
    """
    # 1. 取得篩選參數
    # 2. 呼叫 Model 取得資料
    # 3. 渲染 index.html
    pass

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """
    接收新增任務表單。
    """
    # 1. 取得表單內容
    # 2. 呼叫 Model 新增任務
    # 3. 重新導向回首頁
    pass

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務狀態。
    """
    # 1. 呼叫 Model 切換狀態
    # 2. 重新導向回首頁
    pass

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務。
    """
    # 1. 呼叫 Model 刪除任務
    # 2. 重新導向回首頁
    pass
