from pathlib import Path


class AvatarManager:
    ALLOWED_SIGNATURES = {
        b'\xFF\xD8\xFF': 'jpeg',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'png',
        b'\x47\x49\x46\x38\x37\x61': 'gif',
        b'\x47\x49\x46\x38\x39\x61': 'gif',
        b'\x52\x49\x46\x46': 'webp',
    }

    @staticmethod
    def validate_image(content: bytes) -> bool:
        for signature in AvatarManager.ALLOWED_SIGNATURES.keys():
            if content.startswith(signature):
                if signature == b'\x52\x49\x46\x46':
                    return len(content) >= 12 and content[8:12] == b'WEBP'
                return True
        return False

    @staticmethod
    def delete_avatar(db_path: str, upload_root: Path) -> bool:
        try:
            clean_path = db_path.replace("backend/", "").replace("\\", "/")

            if not clean_path.startswith("uploads/avatars/"):
                return False

            filename = clean_path.split("/")[-1]
            if ".." in filename or "/" in filename or "\\" in filename:
                return False

            file_path = upload_root / "avatars" / filename
            expected_parent = (upload_root / "avatars").resolve()

            if file_path.resolve().parent != expected_parent:
                return False

            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                return True

            return False
        except (ValueError, OSError):
            return False
