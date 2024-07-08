from fastapi import APIRouter

from src.application.core.fastapi.custom_json_response import CustomORJSONResponse
from src.application.core.fastapi.pydantic_models import ResponseBaseModel
from src.application.domain.auth.views import auth_router
from src.application.domain.home.views import home_router
from src.application.domain.user.views import user_router as user_v1_router


class ErrorResponse(ResponseBaseModel):
    code: str
    message: str
    data: dict | list | None


router = APIRouter(
    default_response_class=CustomORJSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(home_router, tags=["Home"])
