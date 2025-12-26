# EvoSystem

一個現代化的全端會員管理系統。

## 技術棧

### 後端
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- JWT 認證

### 前端
- Vue 3
- Vite
- Tailwind CSS v4
- Vue Router
- Axios

## 功能

- 用戶註冊與登入
- 個人資料管理
- 頭像上傳
- 用戶管理（管理員）
- 響應式設計

## 安裝與運行

### 後端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 環境配置

複製 `.env.example` 為 `.env` 並配置相關參數：
- 資料庫連線
- JWT 密鑰
- CORS 設定

## 授權

MIT
