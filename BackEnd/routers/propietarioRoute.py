from fastapi import APIRouter, Depends, HTTPException
from controllers import propietarioController, propiedadController
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

@router.get("/", response_model=list[schemas.Propietario], description="Obtener la lista de propietarios")
async def get_Propietarios(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    res = await propietarioController.getPropietarios(db, skip=skip, limit=limit)
    return res

@router.get("/{id}", response_model=schemas.Arrendatario, description="Obtener un propietario por Id")
async def get_Propietario(id: int, db: Session = Depends(get_db)):
    res = await propietarioController.getPropietarioById(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="Propietario not found")
    return res

@router.post("/")
async def create_Propietario(prop: schemas.PropietarioCreate, db: Session = Depends(get_db)):
    db_prop = await propietarioController.getPropietarioByRFC(db, rfc=prop.rfc)
    if db_prop:
        raise HTTPException(status_code=400, detail="Propietario already exists")
    res = await propietarioController.insertPropietario(db=db, propietario=prop)
    return res

@router.delete("/{id}")
async def delete_Propietario(id: int, db: Session = Depends(get_db)):
    db_Prop = await propietarioController.getPropietarioById(db, id)
    if db_Prop is None:
        raise HTTPException(status_code=400, detail="Propietario does not exist")
    res = await propietarioController.deletePropietario(db, id)
    return res

@router.put("{id},{id_propiedad}")
async def insert_Propiedad(id: int, id_propiedad: int, db: Session = Depends(get_db)):
    db_propietario = await propietarioController.getPropietarioById(db, id)
    db_propiedad = await propiedadController.getPropiedadById(db, id_propiedad)
    if db_propietario is None:
        raise HTTPException(status_code=400, detail="Propietario does not exist")
    elif db_propiedad is None:
        raise HTTPException(status_code=400, detail="Propiedad do not exist")
    res = await propietarioController.insertProp_Propiedad(db, db_propietario, db_propiedad)
    return res