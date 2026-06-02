from fastapi import APIRouter, Depends
from modulos.auth.schemas import UserRegister
from modulos.auth.register.service import register_user
from shared.security.dependencies import get_current_admin


#-----------------
# API REGISTER
#-----------------

router = APIRouter(tags=["auth"])

@router.post("/auth/register", status_code=201)
def register_endpoint(data: UserRegister,
					admin = Depends(get_current_admin)):
	return register_user(data)
