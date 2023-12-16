import datetime
import pytz
from flask import Flask, render_template
from google.cloud import datastore

# 創建 Flask 應用實例。
app = Flask(__name__)

# 創建 Google Cloud Datastore 客戶端實例。
datastore_client = datastore.Client()

@app.route("/")
def root():
    # 獲取當前的台灣時間（台北時間，UTC+8）
    # taiwan_tz = pytz.timezone('Asia/Taipei')
    taiwan_tz = datetime.timezone(datetime.timedelta(hours=8))
    taiwan_time = datetime.datetime.now(tz=taiwan_tz)

    # 將台灣時間存儲到 Datastore
    store_time(taiwan_time)

    # 從 Datastore 獲取最近的訪問時間。
    times = fetch_times(10)

    # 使用從 Datastore 獲取的時間渲染並返回 HTML 模板。
    return render_template("index.html", times=times)

def store_time(dt):
    # 創建一個新的 Datastore 實體來存儲訪問時間。
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update({"timestamp": dt})

    # 將實體保存到 Datastore。
    datastore_client.put(entity)

def fetch_times(limit):
    # 從 Datastore 查詢訪問時間。
    query = datastore_client.query(kind="visit")
    query.order = ["-timestamp"]

    # 獲取最近的限定數量的訪問時間。
    times = query.fetch(limit=limit)

    return times

if __name__ == "__main__":
    # 這段代碼僅在本地運行 Flask 應用時使用。
    # 當部署到 Google App Engine 時，會使用不同的 web server（如 Gunicorn）來運行此應用。
    # 靜態文件（如 CSS, JavaScript）將自動從 Flask 的 "static" 目錄中提供。
    # 詳情可參見 Flask 文檔。
    app.run(host="127.0.0.1", port=8080, debug=True)
