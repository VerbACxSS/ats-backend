from fastapi import APIRouter

from .routers import healthcheck_router
from .routers import prediction_router

router = APIRouter()

router.include_router(healthcheck_router.router, prefix='/healthcheck', tags=['health-check'])
router.include_router(prediction_router.router, prefix='/predict', tags=['predict'])