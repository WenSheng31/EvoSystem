from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from pathlib import Path
from ...core.security import get_current_user, get_password_hash, verify_password
from ...core.database import get_db
from ...core.config import settings
from ...core.file_utils import AvatarManager
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / settings.UPLOAD_DIR / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用戶名已被使用"
            )
        current_user.username = user_update.username

    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="郵箱已被使用"
            )
        current_user.email = user_update.email

    if user_update.bio is not None:
        current_user.bio = user_update.bio

    if user_update.password:
        if not user_update.old_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="修改密碼需要提供舊密碼"
            )
        if not verify_password(user_update.old_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="舊密碼錯誤"
            )
        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的檔案格式，允許: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="檔案大小超過 5MB"
        )

    if not AvatarManager.validate_image(contents):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無效的圖片檔案"
        )

    if current_user.avatar:
        AvatarManager.delete_avatar(current_user.avatar, UPLOAD_DIR.parent)

    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(contents)

    current_user.avatar = f"uploads/avatars/{filename}"
    db.commit()
    db.refresh(current_user)

    return current_user
