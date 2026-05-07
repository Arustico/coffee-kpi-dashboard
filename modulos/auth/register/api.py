from fastapi import APIRouter
from modulos.auth.schemas import UserRegister
from modulos.auth.register.service import register_user

router = APIRouter(tags=["auth"])

@router.post("/auth/register", status_code=201)
def register_endpoint(data: UserRegister):
	return register_user(data)
