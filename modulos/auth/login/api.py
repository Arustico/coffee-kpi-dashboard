from fastapi import APIRouter
from modulos.auth.schemas import UserLogin
from modulos.auth.login.service import login_user


router = APIRouter(tags=["auth"])

@router.post("/auth/login")
def login_endpoint(data: UserLogin):
	return login_user(data)
