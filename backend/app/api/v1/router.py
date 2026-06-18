from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.cards import router as cards_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.insights import router as insights_router
from app.api.v1.endpoints.transactions import router as transactions_router
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(cards_router, prefix="/cards", tags=["cards"])
api_router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(insights_router, prefix="/insights", tags=["insights"])
