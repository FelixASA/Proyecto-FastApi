from fastapi import APIRouter, Depends, HTTPException
from controllers import arrendatarioController, propiedadController
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
    prefix="/arrendatario",
    tags=["arrendatario"]
)

@router.get("/", response_model=list[schemas.Arrendatario])
async def get_Arrendatarios(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    res = await arrendatarioController.getArrendatarios(db, skip=skip, limit=limit)
    return res

@router.get("/{id}", response_model=schemas.Arrendatario)
async def get_Arrendatario(id: int, db: Session = Depends(get_db)):
    res = await arrendatarioController.getArrendatariosById(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="Arrendatario not found")
    return res

@router.post("/")
async def create_Arrendatario(arren: schemas.ArrendatarioCreate, db: Session = Depends(get_db)):
    db_Arren = await arrendatarioController.getArrendatarioByRFC(db, rfc=arren.rfc)
    if db_Arren:
        raise HTTPException(status_code=400, detail="Arrendatario already exists")
    res = await arrendatarioController.insertArrendatario(db=db, arrendatario=arren)
    return res

@router.delete("/{id}")
async def delete_Arrendatario(id: int, db: Session = Depends(get_db)):
    db_Arren = await arrendatarioController.getArrendatariosById(db, id)
    if db_Arren is None:
        raise HTTPException(status_code=400, detail="Arrendatario does not exist")
    res = await arrendatarioController.deleteArrendatario(db, id)
    return res

@router.put("/{id},{id_prop}", response_model=schemas.Arrendatario)
async def insert_Propiedad(id: int, id_prop:int, db: Session = Depends(get_db)):
    db_prop = await propiedadController.getPropiedadById(db=db, id=id_prop)
    db_arren = await arrendatarioController.getArrendatariosById(db, id)
    if db_prop is None:
        raise HTTPException(status_code=400, detail="Propiedad does not exist")
    elif db_arren is None:
        raise HTTPException(status_code=400, detail="Arrendatario do not exist")
    res = await arrendatarioController.insertArren_Propiedad(db=db, arren=db_arren, propiedad=db_prop)
    return res