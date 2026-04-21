from app import create_app

# 建立應用程式實體
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器，預設埠號為 5000
    # debug=True 指令會讓伺服器在程式碼變更時自動重啟
    app.run(debug=True)
