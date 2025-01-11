from fastapi import APIRouter
from .auth import route as auth_router
from .inference import route as inference_router
from .user import route as user_router

# 공통 prefix를 설정
router = APIRouter(prefix="/api/v1")

# 각 라우트를 포함
router.include_router(auth_router)
router.include_router(inference_router)
router.include_router(user_router)
