from fastapi import APIRouter, Depends, Response

from src.application.core.authority.permissions import AllowAll
from src.application.core.dependencies import PermissionDependency
from src.application.core.fastapi.log_route import LogRoute

home_router = APIRouter(route_class=LogRoute)


@home_router.get("/health", dependencies=[Depends(PermissionDependency([AllowAll]))])
async def home():
    return Response(status_code=200)
