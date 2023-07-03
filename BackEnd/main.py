from fastapi import FastAPI
from routers import arrendatarioRoute, propietarioRoute, propiedadRoute
from sql_app import models
from sql_app.database import engine
import sqlalchemy
from fastapi.routing import APIRouter

router = APIRouter()

#metadata = sqlalchemy.MetaData()
#metadata.create_all(engine)
#models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(arrendatarioRoute.router)
app.include_router(propietarioRoute.router)
app.include_router(propiedadRoute.router)

@app.get("/")
async def root(): 
    return {"message: Hello World"}