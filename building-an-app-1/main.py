import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    # 為了示例，使用靜態模擬資料來填充模板。
    # 這將在後續步驟中被實際真實資料替換。
    dummy_times = [
        datetime.datetime(2018, 1, 1, 10, 0, 0),
        datetime.datetime(2018, 1, 2, 10, 30, 0),
        datetime.datetime(2018, 1, 3, 11, 0, 0),
    ]

    return render_template("index.html", times=dummy_times)

if __name__ == "__main__":
    # 這僅在本地運行時使用。部署到Google App Engine時，
    # 一個如 Gunicorn 之類的網絡服務器進程會服務於此應用。
    # 可以通過在 app.yaml 中添加 `entrypoint` 來配置。
    # Flask 的開發服務器會自動服務於 "static" 目錄中的靜態文件。
    # 參見：http://flask.pocoo.org/docs/1.0/quickstart/#static-files。
    # 一旦部署，App Engine 本身將如 app.yaml 中所配置的那樣服務這些文件。
    app.run(host="127.0.0.1", port=8080, debug=True)
