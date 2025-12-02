from fastapi import FastAPI
from database import Base, engine
from modules.items.routes import (
    createItem,
    readItem,
    updateItem,
    deleteItem,
    analytics,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(createItem.router)
app.include_router(readItem.router)
app.include_router(updateItem.router)
app.include_router(deleteItem.router)
app.include_router(analytics.router) 