from fastapi import APIRouter
from modulos.auth.schemas import TokenRefreshRequest
from modulos.auth.refresh.service import refresh_access_token

router = APIRouter(tags=["auth"])

@router.post("/auth/refresh")
def refresh_endpoint(data: TokenRefreshRequest):
	return refresh_access_token(data)
