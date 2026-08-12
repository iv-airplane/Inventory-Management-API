from pydantic import BaseModel, ConfigDict
# Pydantic models for input and output validation

# Pydantic model for the request body
class ItemCreate(BaseModel):
    name: str
    price: float

# Pydantic model for the response body
class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    in_stock: bool
