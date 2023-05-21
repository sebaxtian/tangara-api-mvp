from pydantic import BaseModel


class LugaresSchema(BaseModel):
    id: str
    nombre: str
