from fastapi import APIRouter
from .auth import router as auth_router


# 공통 prefix를 설정
router = APIRouter(prefix="/api/v1")

# 각 라우트를 포함
router.include_router(auth_router)
