import os
from flask import Flask
from .routes.tasks import tasks_bp

def create_app():
    """
    應用程式工廠：初始化 Flask 並註冊路由與設定。
    """
    # 建立 Flask 實體，instance_relative_config=True 讓設定檔案可以放在 instance 資料夾
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY='dev', # 建議在正式環境中從環境變數讀取
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在（用於存放 SQLite 資料庫）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊任務管理模組的 Blueprint
    app.register_blueprint(tasks_bp)

    # 首頁路由通常放在這裡或註冊為獨立 Blueprint
    # 為了測試，我們讓 Blueprint 處理根目錄 /
    
    return app
