# App Engine Standard Version - python Quick Start

此專案為 AppEngine 的快速實作，參考官方提供案例實作，在標準版本下 Python 實作 Flask 簡單網頁模板。 

## 功能版本

1. 最初實作，在本地進行功能測試，並將第一版部署至 App Engine
2.

## 先決條件

1. 本地測試已安裝 python 3, 筆者當下實作版本為 python 3.10.6


## 實作

### 下載 repository
```git clone https://github.com/Whaleman0423/app_engine_quick_start.git```

### building-an-app-1

#### 本地測試指令
```
cd app_engine_quick_start
python -m venv venv

# windows
.\venv\Scripts\activate

cd building-an-app-1
pip install -r requirements.txt
python main.py

<!-- 訪問 localhost:8080 -->
http://localhost:8080
```

#### 部署至 app engine
至 Cloud Shell

在空目錄 git clone

```
cd app_engine_quick_start/building-an-app-1
```

部署

```
gcloud app deploy
```

### building-an-app-2
