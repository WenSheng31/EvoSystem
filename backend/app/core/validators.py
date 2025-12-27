"""
統一的驗證器
避免在多個 Schema 中重複驗證邏輯
"""
import re


class PasswordValidator:
    """密碼驗證器"""
    MIN_LENGTH = 8
    MAX_LENGTH = 50

    @staticmethod
    def validate(password: str) -> str:
        """
        驗證密碼強度

        規則：
        - 長度：8-50 個字符
        - 必須包含至少一個字母
        - 必須包含至少一個數字

        Args:
            password: 待驗證的密碼

        Returns:
            str: 驗證通過的密碼

        Raises:
            ValueError: 密碼不符合要求
        """
        if len(password) < PasswordValidator.MIN_LENGTH:
            raise ValueError(f'密碼至少需要 {PasswordValidator.MIN_LENGTH} 個字符')

        if len(password) > PasswordValidator.MAX_LENGTH:
            raise ValueError(f'密碼最多 {PasswordValidator.MAX_LENGTH} 個字符')

        if not re.search(r'[A-Za-z]', password):
            raise ValueError('密碼必須包含至少一個字母')

        if not re.search(r'\d', password):
            raise ValueError('密碼必須包含至少一個數字')

        return password


class UsernameValidator:
    """用戶名驗證器"""
    MAX_LENGTH = 20
    PATTERN = r'^[\w\u4e00-\u9fa5]+$'

    @staticmethod
    def validate(username: str) -> str:
        """
        驗證用戶名

        規則：
        - 長度：1-20 個字符
        - 只允許字母、數字、下劃線和中文

        Args:
            username: 待驗證的用戶名

        Returns:
            str: 驗證通過的用戶名

        Raises:
            ValueError: 用戶名不符合要求
        """
        if not username or len(username.strip()) == 0:
            raise ValueError('用戶名不能為空')

        if len(username) > UsernameValidator.MAX_LENGTH:
            raise ValueError(f'用戶名最多 {UsernameValidator.MAX_LENGTH} 個字符')

        if not re.match(UsernameValidator.PATTERN, username):
            raise ValueError('用戶名只能包含字母、數字、下劃線和中文')

        return username
