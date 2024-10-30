from pydantic import BaseModel


class RestaurantBase(BaseModel):
    restaurant_name: str
    working_hours: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int


class RestaurantNameRead(BaseModel):
    restaurant_name: str

    class Config:
        from_attributes = True

