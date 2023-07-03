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

async def getArrendatarios(db: Session, skip: int=0, limit: int=100):
    arrendatarios = db.query(models.Arrendatario).offset(skip).limit(limit).all()
    return arrendatarios

async def getArrendatariosById(db: Session, id: int):
    arrendatario = db.query(models.Arrendatario).filter(models.Arrendatario.id == id).first()
    return arrendatario

async def getArrendatarioByRFC(db: Session, rfc: str):
    return db.query(models.Arrendatario).filter(models.Arrendatario.rfc == rfc).first()

async def insertArrendatario(db: Session, arrendatario: schemas.ArrendatarioCreate):
    db_arren = models.Arrendatario(rfc=arrendatario.rfc, nombre=arrendatario.nombre, apellido=arrendatario.apellido)
    db.add(db_arren)
    db.commit()
    db.refresh(db_arren)
    return db_arren

async def deleteArrendatario(db: Session, id: int):
    db_arren = db.query(models.Arrendatario).filter(models.Arrendatario.id == id).first()
    db.query(models.Arrendatario).filter(models.Arrendatario.id == id).delete()
    return db_arren

async def insertArren_Propiedad(db: Session, arren: models.Arrendatario, propiedad: models.Propiedad):
    propiedad.arrendatario = arren
    arren.propiedades.append(propiedad)
    db.commit()
    db.refresh(arren)
    db.refresh(propiedad)
    return arren
    