"""
統一的文件操作工具
避免在多個路由中重複文件處理邏輯
"""
from pathlib import Path
from typing import Optional


class AvatarManager:
    """頭像文件管理器"""
    ALLOWED_PREFIX = "backend/uploads/avatars/"

    @staticmethod
    def is_safe_path(avatar_path: str, upload_dir: Path) -> bool:
        """
        檢查文件路徑是否安全

        防止路徑穿越攻擊（Path Traversal）

        Args:
            avatar_path: 頭像路徑（如："backend/uploads/avatars/xxx.jpg"）
            upload_dir: 上傳目錄的絕對路徑

        Returns:
            bool: 路徑是否安全
        """
        # 檢查前綴
        if not avatar_path.startswith(AvatarManager.ALLOWED_PREFIX):
            return False

        # 提取文件名
        filename = avatar_path.split("/")[-1]

        # 檢查文件名中是否包含危險字符
        if ".." in filename or "/" in filename or "\\" in filename:
            return False

        # 檢查解析後的路徑是否在允許的目錄內
        avatar_file = upload_dir / filename
        try:
            return avatar_file.resolve().parent == upload_dir.resolve()
        except (ValueError, OSError):
            return False

    @staticmethod
    def delete_avatar(avatar_path: str, upload_dir: Path) -> bool:
        """
        安全地刪除頭像文件

        Args:
            avatar_path: 頭像路徑（如："backend/uploads/avatars/xxx.jpg"）
            upload_dir: 上傳目錄的絕對路徑

        Returns:
            bool: 是否成功刪除
        """
        try:
            # 安全性檢查
            if not AvatarManager.is_safe_path(avatar_path, upload_dir):
                return False

            # 提取文件名並構建完整路徑
            filename = avatar_path.split("/")[-1]
            avatar_file = upload_dir / filename

            # 刪除文件
            if avatar_file.exists() and avatar_file.is_file():
                avatar_file.unlink()
                return True

            return False
        except OSError:
            # 文件刪除失敗（權限問題、文件被占用等）
            return False

    @staticmethod
    def get_filename_from_path(avatar_path: str) -> Optional[str]:
        """
        從頭像路徑中提取文件名

        Args:
            avatar_path: 頭像路徑（如："backend/uploads/avatars/xxx.jpg"）

        Returns:
            Optional[str]: 文件名，如果路徑無效則返回 None
        """
        if not avatar_path or not avatar_path.startswith(AvatarManager.ALLOWED_PREFIX):
            return None

        return avatar_path.split("/")[-1]
