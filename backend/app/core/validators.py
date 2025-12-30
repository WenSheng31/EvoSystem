import re


class PasswordValidator:
    MIN_LENGTH = 8
    MAX_LENGTH = 12

    @staticmethod
    def validate(password: str) -> str:
        if len(password) < PasswordValidator.MIN_LENGTH:
            raise ValueError(f'密碼至少需要 {PasswordValidator.MIN_LENGTH} 個字符')

        if len(password) > PasswordValidator.MAX_LENGTH:
            raise ValueError(f'密碼最多 {PasswordValidator.MAX_LENGTH} 個字符')

        if not re.search(r'[A-Za-z]', password):
            raise ValueError('密碼必須包含至少一個英文字母')

        return password


class UsernameValidator:
    MAX_LENGTH = 20
    PATTERN = r'^[\w\u4e00-\u9fa5]+$'

    @staticmethod
    def validate(username: str) -> str:
        if not username or len(username.strip()) == 0:
            raise ValueError('用戶名不能為空')

        if len(username) > UsernameValidator.MAX_LENGTH:
            raise ValueError(f'用戶名最多 {UsernameValidator.MAX_LENGTH} 個字符')

        if not re.match(UsernameValidator.PATTERN, username):
            raise ValueError('用戶名只能包含字母、數字、下劃線和中文')

        return username
