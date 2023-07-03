from sqlalchemy.orm import Session
from fastapi import Depends
from sql_app import models, schemas
from sql_app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def getPropietarios(db: Session, skip: int=0, limit: int=100):
    propietarios = db.query(models.Propietario).offset(skip).limit(limit).all()
    return propietarios

async def getPropietarioById(db: Session, id: int):
    propietario = db.query(models.Propietario).filter(models.Propietario.id == id).first()
    return propietario

async def getPropietarioByRFC(db: Session, rfc: str):
    return db.query(models.Propietario).filter(models.Propietario.rfc == rfc).first()

async def insertPropietario(db: Session, propietario: schemas.ArrendatarioCreate):
    db_prop = models.Propietario(rfc=propietario.rfc, nombre=propietario.nombre, apellido=propietario.apellido)
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

async def deletePropietario(db: Session, id: int):
    db_prop = db.query(models.Propietario).filter(models.Propietario.id == id).first()
    db.query(models.Propietario).filter(models.Propietario.id == id).delete()
    return db_prop

async def insertProp_Propiedad(db: Session, propietario: models.Propietario, propiedad: models.Propiedad):
    propiedad.propietarios.append(propietario)
    propietario.propiedades_prop.append(propiedad)
    db.commit()
    db.refresh(propiedad)
    db.refresh(propietario)
    return propietario