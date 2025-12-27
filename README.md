# EvoSystem

一個現代化的全端會員管理系統，提供完整的用戶管理、個人資料編輯、待辦事項管理等功能。

## ✨ 功能特色

### 用戶功能
- 🔐 用戶註冊與登入（JWT 認證）
- 👤 個人資料管理（用戶名、郵箱、個人簡介）
- 🖼️ 頭像上傳（支援 JPG, PNG, GIF, WebP，最大 5MB）
- ✅ 待辦事項管理
  - 新增、編輯、刪除待辦事項
  - 完成狀態切換
  - 行內編輯功能
  - 私有數據（每個用戶只能看到自己的待辦事項）

### 管理員功能
- 👥 用戶管理
  - 查看所有用戶列表
  - 啟用/停用用戶帳號
  - 重置用戶密碼
  - 刪除用戶

### UI/UX
- 📱 完全響應式設計（支援桌面和行動裝置）
- 🎨 統一的設計系統（Tailwind CSS）
- 🔔 Toast 通知系統
- ❓ 確認對話框
- 🎯 直觀的側邊欄導航

## 🛠️ 技術棧

### 後端
- **框架**: FastAPI (Python)
- **資料庫**: PostgreSQL
- **ORM**: SQLAlchemy
- **認證**: JWT (python-jose)
- **密碼加密**: bcrypt + passlib
- **API 文檔**: 自動生成 Swagger UI / ReDoc

### 前端
- **框架**: Vue 3 (Composition API)
- **建置工具**: Vite
- **UI 框架**: Tailwind CSS v4
- **路由**: Vue Router
- **HTTP 客戶端**: Axios
- **圖標**: lucide-vue-next
- **狀態管理**: Composables (useUser, useToast, useConfirmDialog)

## 📦 安裝與運行

### 前置要求
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 1. 克隆專案

```bash
git clone https://github.com/WenSheng31/EvoSystem.git
cd EvoSystem
```

### 2. 後端設定

```bash
cd backend

# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 安裝依賴
pip install -r requirements.txt

# 配置環境變數
# 複製 .env.example 為 .env 並填入資料庫連線等資訊
cp .env.example .env

# 啟動後端服務 (http://localhost:8000)
python run.py
```

**環境變數範例** (`.env`):
```env
DATABASE_URL=postgresql://username:password@localhost/evosystem
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. 前端設定

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發服務器 (http://localhost:5173)
npm run dev

# 建置生產版本
npm run build
```

### 4. 資料庫設定

1. 建立 PostgreSQL 資料庫：
```sql
CREATE DATABASE evosystem;
```

2. 後端會在首次啟動時自動建立所需的資料表（SQLAlchemy auto-create）

## 📁 專案結構

```
EvoSystem/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/      # API 路由 (auth, users, admin, todos)
│   │   ├── core/            # 核心配置 (config, database, security)
│   │   ├── models/          # SQLAlchemy 資料模型
│   │   └── schemas/         # Pydantic 請求/回應模型
│   ├── uploads/             # 檔案上傳目錄
│   ├── requirements.txt
│   └── run.py              # 應用入口
│
└── frontend/
    ├── src/
    │   ├── api/            # API 請求封裝
    │   ├── components/     # 全局組件 (Toast, Dialog, Sidebar)
    │   ├── composables/    # 可組合函數
    │   ├── config/         # 配置常量
    │   ├── layouts/        # 布局組件
    │   ├── router/         # 路由配置
    │   └── views/          # 頁面組件
    ├── public/
    └── package.json
```

## 🚀 API 文檔

後端啟動後，可以訪問以下 URL 查看 API 文檔：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 預設帳號

系統需要手動註冊第一個用戶。要建立管理員帳號，需要在資料庫中手動將用戶的 `role` 欄位設為 `admin`。

## 📝 主要路由

### 前端路由
- `/login` - 登入頁
- `/register` - 註冊頁
- `/home` - 首頁（需認證）
- `/todos` - 待辦事項（需認證）
- `/account` - 帳號管理（需認證）
- `/admin` - 用戶管理（需管理員權限）

### API 端點
- `POST /api/register` - 用戶註冊
- `POST /api/login` - 用戶登入
- `GET /api/me` - 獲取當前用戶資料
- `PATCH /api/me` - 更新個人資料
- `POST /api/avatar` - 上傳頭像
- `GET /api/todos` - 獲取待辦事項
- `POST /api/todos` - 建立待辦事項
- `PATCH /api/todos/{id}` - 更新待辦事項
- `DELETE /api/todos/{id}` - 刪除待辦事項
- `GET /api/admin/users` - 獲取所有用戶（管理員）
- `PATCH /api/admin/users/{id}/toggle-active` - 切換用戶狀態（管理員）
- `POST /api/admin/users/{id}/reset-password` - 重置密碼（管理員）
- `DELETE /api/admin/users/{id}` - 刪除用戶（管理員）

## 🎨 設計規範

- **邊框**: `border-gray-200` (主容器), `border-gray-300` (輸入框)
- **圓角**: 統一使用 `rounded-lg` (0.5rem)
- **主色**: 灰色系 (`gray-900` 為主要按鈕顏色)
- **字體**: 系統預設字體
- **間距**: 遵循 Tailwind 的間距系統

## 🔒 安全性

- 密碼使用 bcrypt 加密
- JWT Token 30 分鐘過期
- 路由守衛防止未授權訪問
- CORS 配置限制
- SQL Injection 防護（使用 ORM）
- XSS 防護（Vue 自動轉義）

## 📄 開發文檔

更詳細的開發指南請參考 `CLAUDE.md` 文件。

## 📄 授權

MIT License
