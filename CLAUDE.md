# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個全端會員系統，使用 FastAPI (Python) 後端和 Vue 3 前端。系統提供用戶註冊、登入、個人資料管理和頭像上傳功能。

## 技術架構

### 後端 (FastAPI)
- **框架**: FastAPI + Uvicorn
- **資料庫**: PostgreSQL (使用 SQLAlchemy ORM)
- **認證**: JWT (使用 python-jose)
- **密碼加密**: bcrypt + passlib
- **結構**:
  - `app/main.py`: 應用入口，註冊路由和中介軟體
  - `app/core/`: 核心功能 (config, database, security)
  - `app/models/`: SQLAlchemy 資料模型
  - `app/schemas/`: Pydantic 請求/回應模型
  - `app/api/routes/`: API 路由處理器 (auth.py, users.py)

### 前端 (Vue 3)
- **框架**: Vue 3 + Vue Router
- **建置工具**: Vite
- **UI 框架**: Tailwind CSS v4
- **HTTP 客戶端**: Axios
- **結構**:
  - `src/router/index.js`: 路由配置和認證守衛
  - `src/views/`: 頁面組件 (Login, Register, Home, Account)
  - `src/api/auth.js`: API 請求封裝，包含 JWT token 攔截器
  - `src/composables/`: 可組合函數
  - `src/components/`: 可重用組件

## 開發指令

### 後端
```bash
# 安裝依賴
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt

# 啟動開發伺服器 (http://localhost:8000)
python run.py

# 資料庫設定
# 需先建立 PostgreSQL 資料庫: member_system
# 連線資訊在 app/core/config.py
```

### 前端
```bash
# 安裝依賴
cd frontend
npm install

# 啟動開發伺服器 (http://localhost:5173)
npm run dev

# 建置生產版本
npm run build

# 預覽生產建置
npm run preview
```

## 重要配置

### 資料庫連線
- 預設配置在 `backend/app/core/config.py`
- 預設連線: `postgresql://postgres:889753@localhost/member_system`
- 可透過 `.env` 檔案覆蓋設定

### JWT 認證
- Token 儲存在 localStorage (key: "token")
- 前端請求攔截器自動附加 `Authorization: Bearer <token>`
- Token 有效期限: 30 分鐘 (可在 config.py 調整)

### 檔案上傳
- 頭像上傳路徑: `backend/uploads/avatars/`
- 靜態檔案透過 FastAPI StaticFiles 在 `/uploads` 路徑提供

### API 代理
- Vite 開發伺服器將 `/api` 請求代理到後端 `http://localhost:8000`
- 前端 API 基礎路徑設為 `/api` (在 src/api/auth.js)

## 資料模型

### User (users 表)
- id: Integer (主鍵)
- username: String (唯一，索引)
- email: String (唯一，索引)
- hashed_password: String
- avatar: String (可選)
- created_at: DateTime
- updated_at: DateTime

## API 端點

所有端點前綴: `/api`

- `POST /api/register`: 註冊新用戶
- `POST /api/login`: 用戶登入，返回 JWT token
- `GET /api/me`: 取得當前用戶資料 (需認證)
- `PUT /api/update-profile`: 更新個人資料 (需認證)
- `POST /api/upload-avatar`: 上傳頭像 (需認證)

## 路由與認證

### 前端路由
- `/login`: 登入頁
- `/register`: 註冊頁
- `/home`: 首頁 (需認證)
- `/account`: 帳號管理 (需認證)

### 路由守衛
- 已在 `src/router/index.js` 實作
- 需認證頁面標記 `meta: { requiresAuth: true }`
- 無 token 時自動重定向到 `/login`
- 已登入用戶訪問登入/註冊頁會重定向到 `/home`

## 安全性與驗證

- **密碼安全**：使用 bcrypt 加密，要求至少 8 個字符且包含字母和數字
- **用戶名驗證**：長度 3-20 字符，只允許字母、數字、下劃線和中文
- **環境變數**：所有敏感設定必須透過 `.env` 檔案配置（參考 `.env.example`）
- **CORS 限制**：僅允許特定方法和標頭，不使用萬用字符
- **Token 管理**：JWT token 自動過期處理，失效時自動跳轉登入頁

## 代碼架構規範

### 前端架構
- **Composables**：共用邏輯放在 `src/composables/`（如 `useUser.js`）
- **配置管理**：常量統一在 `src/config/constants.js` 管理
- **API 調用**：使用 `authAPI` 方法，不直接調用 axios
- **錯誤處理**：401 錯誤由 response interceptor 統一處理

### 後端架構
- **配置優先**：所有可配置項放在 `core/config.py`
- **環境變數**：敏感資訊必須從 `.env` 讀取
- **驗證邏輯**：使用 Pydantic validators 在 schemas 層驗證
- **文件上傳**：配置統一在 settings，路徑使用配置項

## 常見開發任務

### 新增 API 端點
1. 在 `backend/app/schemas/user.py` 定義請求/回應模型（含驗證器）
2. 在 `backend/app/api/routes/` 建立或修改路由檔案
3. 在 `backend/app/main.py` 註冊新路由
4. 在 `frontend/src/api/auth.js` 的 `authAPI` 添加對應方法

### 新增前端頁面
1. 在 `frontend/src/views/` 建立 Vue 組件
2. 使用 `useUser` composable 管理用戶狀態
3. 從 `config/constants.js` 導入路由常量
4. 在 `frontend/src/router/index.js` 註冊路由
5. 如需認證，加入 `meta: { requiresAuth: true }`

### 修改資料模型
1. 更新 `backend/app/models/user.py`
2. 更新對應的 `backend/app/schemas/user.py`（含驗證器）
3. 重啟後端會自動同步資料表（開發階段）

### 添加新的配置項
1. **後端**：在 `backend/app/core/config.py` 的 `Settings` 類添加
2. **前端**：在 `frontend/src/config/constants.js` 添加常量
3. 更新 `.env.example` 文件作為參考
