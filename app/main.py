import uvicorn
from fastapi import FastAPI

from app.api.routes.cats_routes import router as cats_router
from app.api.routes.missions_routes import router as missions_router
from app.config.config import settings
from app.core.db.database import create_db_and_tables

create_db_and_tables()

app: FastAPI = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router=cats_router, prefix=settings.API_V1_STR)
app.include_router(router=missions_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
