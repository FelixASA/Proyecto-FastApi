from pydantic import BaseModel

class PropiedadBase(BaseModel):
    clave_catastral: str
    descripcion: str

class PropietarioBase(BaseModel):
    rfc: str
    nombre: str
    apellido: str

class ArrendatarioBase(BaseModel):
    rfc: str
    nombre: str
    apellido: str

class PropiedadCreate(PropiedadBase):
    pass

class ArrendatarioCreate(ArrendatarioBase):
    pass

class PropietarioCreate(PropietarioBase):
    pass


class Propiedad(PropiedadBase):
    id: int
    arrendatario_id: int
    propietarios: list[PropietarioBase] = []

    class Config:
        orm_mode = True

class Arrendatario(ArrendatarioBase):
    id: int
    propiedades: list[PropiedadBase] = []

    class Config:
        orm_mode = True

class Propietario(PropietarioBase):
    id: int
    propiedades_prop: list[PropiedadBase] = []

    class Config:
        orm_mode = True