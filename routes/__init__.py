from routes.read import router as read_router
from routes.create import router as create_router
from routes.update import router as update_router
from routes.delete import router as delete_router
from routes.analytics import router as analytics_router

__all__ = ["read", "create", "update", "delete", "analytics"]
