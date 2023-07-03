from fastapi import APIRouter, Depends, HTTPException
from controllers import propiedadController, arrendatarioController
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
    prefix="/propiedad",
    tags=["propiedad"]
)

@router.get("/", response_model=list[schemas.Propiedad])
async def get_Propiedades(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    res = await propiedadController.getPropiedades(db, skip=skip, limit=limit)
    return res

@router.get("/{id}", response_model=schemas.Propiedad)
async def get_Propiedad(id: int, db: Session = Depends(get_db)):
    res = await propiedadController.getPropiedadById(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="Propiedad not found")
    return res

@router.post("/")
async def create_Propiedad(propiedad: schemas.PropiedadCreate, db: Session = Depends(get_db)):
    db_prop = await propiedadController.getPropiedadByClave(db, clave=propiedad.clave_catastral)
    if db_prop:
        raise HTTPException(status_code=400, detail="Propiedad already exists")
    res = await propiedadController.insertPropiedad(db=db, propiedad=propiedad)
    return res

@router.delete("/{id}")
async def delete_Propiedad(id: int, db: Session = Depends(get_db)):
    db_Prop = await propiedadController.getPropiedadById(db, id)
    if db_Prop is None:
        raise HTTPException(status_code=400, detail="Propiedad does not exist")
    res = await propiedadController.deletePropiedad(db, id)
    return res

@router.put("/arren/{id},{id_arren}", response_model=schemas.Propiedad)
async def insert_Arrendatario(id: int, id_arren: int, db: Session = Depends(get_db)):
    db_arren = await arrendatarioController.getArrendatariosById(db, id_arren)
    db_prop = await propiedadController.getPropiedadById(db=db, id=id)
    if db_prop is None:
        raise HTTPException(status_code=400, detail="Propiedad does not exist")
    elif db_arren is None:
        raise HTTPException(status_code=400, detail="Arrendatario do not exist")
    res = await propiedadController.insertProp_Arrendatario(db, db_prop, db_arren)
    return res

@router.put("/prop/{id},{id_propietario}", response_model=schemas.Propiedad)
async def insert_Propiedad(id: int, id_propietario: int, db: Session = Depends(get_db)):
    pass