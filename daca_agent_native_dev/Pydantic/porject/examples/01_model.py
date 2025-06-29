from pydantic import BaseModel

class User(BaseModel):
    id : int
    name: str
    is_active : bool

input_data = {"id": 123, "name": "coding", "is_active": True}   

user = User(**input_data)
print(user)