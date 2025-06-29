from pydantic import BaseModel

class Product (BaseModel):
    id: int
    name: str
    price :float
    is_active: bool

input_Product  = { "id":111, "name": "pizza" , "price": 200 ,"is_active": True}  

product  = Product (**input_Product)
print(product)

