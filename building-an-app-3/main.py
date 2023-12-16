import datetime
import pytz
from flask import Flask, render_template
from google.cloud import datastore
from flask import Flask, render_template, request
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token

# 創建 Flask 應用實例。
app = Flask(__name__)

# 創建 Google Cloud Datastore 客戶端實例。
datastore_client = datastore.Client()

firebase_request_adapter = requests.Request()
@app.route("/")
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

        # Record and fetch the recent times a logged-in user has accessed
        # the site. This is currently shared amongst all users, but will be
        # individualized in a following step.
        store_time(datetime.datetime.now(tz=datetime.timezone.utc))
        times = fetch_times(10)

    return render_template(
        "index.html", user_data=claims, error_message=error_message, times=times
    )


def store_time(dt):
    # 創建一個新的 Datastore 實體來存儲訪問時間。
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update({"timestamp": dt})

    # 將實體保存到 Datastore。
    datastore_client.put(entity)

def fetch_times(limit):
    query = datastore_client.query(kind="visit")
    query.order = ["-timestamp"]

    times_iter = query.fetch(limit=limit)

    # 將迭代器轉換為列表
    times = list(times_iter)

    taiwan_tz = pytz.timezone('Asia/Taipei')

    # 轉換時間為 台灣時間 並格式化為字符串
    formatted_times = []
    for time in times:
        tz_aware_time = time['timestamp'].replace(tzinfo=pytz.utc).astimezone(taiwan_tz)
        formatted_times.append(tz_aware_time.strftime('%Y-%m-%d %H:%M:%S'))
        print(tz_aware_time.strftime('%Y-%m-%d %H:%M:%S'))

    return formatted_times


if __name__ == "__main__":
    # 這段代碼僅在本地運行 Flask 應用時使用。
    # 當部署到 Google App Engine 時，會使用不同的 web server（如 Gunicorn）來運行此應用。
    # 靜態文件（如 CSS, JavaScript）將自動從 Flask 的 "static" 目錄中提供。
    # 詳情可參見 Flask 文檔。
    app.run(host="127.0.0.1", port=8080, debug=True)
