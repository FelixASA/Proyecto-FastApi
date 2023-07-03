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

async def getPropiedades(db: Session, skip: int=0, limit: int=100):
    propiedades = db.query(models.Propiedad).offset(skip).limit(limit).all()
    return propiedades

async def getPropiedadById(db: Session, id: int):
    propiedad = db.query(models.Propiedad).filter(models.Propiedad.id == id).first()
    return propiedad

async def getPropiedadByClave(db: Session, clave: str):
    return db.query(models.Propiedad).filter(models.Propiedad.clave_catastral == clave).first()

async def insertPropiedad(db: Session, propiedad: schemas.PropiedadCreate):
    db_prop = models.Propiedad(clave_catastral = propiedad.clave_catastral, descripcion = propiedad.descripcion)
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

async def deletePropiedad(db: Session, id: int):
    db_prop = db.query(models.Propiedad).filter(models.Propiedad.id == id).first()
    db.query(models.Propiedad).filter(models.Propiedad == id).delete()
    return db_prop

async def insertProp_Arrendatario(db: Session, prop: models.Propiedad, arren: models.Arrendatario):
    prop.arrendatario = arren
    arren.propiedades.append(prop)
    db.commit()
    db.refresh(arren)
    db.refresh(prop)
    return prop

async def insertProp_Propietario(db: Session, prop: models.Propiedad, propietario: models.Propietario):
    prop.propietarios.append(propietario)
    propietario.propiedades_prop.append(prop)
    db.commit()
    db.refresh(prop)
    db.refresh(propietario)
    return prop