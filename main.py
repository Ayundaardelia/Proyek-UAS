from fastapi import FastAPI

from database import Base, engine
from modules.items import models

from modules.items.routes.createItem import router as create_router
from modules.items.routes.readItem import router as read_router
from modules.items.routes.updateItem import router as update_router
from modules.items.routes.deleteItem import router as delete_router
# from modules.items.routes.analytics import router as analytics_router   # MATIKAN DULU

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(create_router)
app.include_router(read_router)
app.include_router(update_router)
app.include_router(delete_router)
# app.include_router(analytics_router)   # MATIKAN DULU

@app.get("/")
def root():
    return {"message": "API is running"}