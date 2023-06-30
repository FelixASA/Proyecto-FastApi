from fastapi import APIRouter, Depends, HTTPException
from controllers import arrendatarioController
from sql_app import models, schemas
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/propietario",
    tags=["propietario"]
)

@router.get("/", response_model=list[schemas.Propietario])
async def get_Propietarios(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    res = { "Get all" }#= await arrendatarioController.getArrendatarios(db, skip=skip, limit=limit)
    return res

@router.get("/{id}")#, response_model=list[schemas.Arrendatario])
async def get_Propietario(id: int, db: Session = Depends(get_db)):
    res = { "Get by id" }
    # res = await arrendatarioController.getArrendatariosById(db, id)
    # if res is None:
    #     raise HTTPException(status_code=404, detail="Arrendatario not found")
    return res

@router.post("/")
async def create_Propietario(arren: schemas.PropietarioCreate, db: Session = Depends(get_db)):
    res = { "Crear" }
    # db_Arren = await arrendatarioController.getArrendatarioByRFC(db, rfc=arren.rfc)
    # if db_Arren:
    #     raise HTTPException(status_code=400, detail="Arrendatario already exists")
    # res = await arrendatarioController.insertArrendatario(db=db, arrendatario=arren)
    return res