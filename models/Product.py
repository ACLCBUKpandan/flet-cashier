from pocketbase.models.utils import BaseModel


class Product(BaseModel):
    id: str
    name: str
    price: float
    image: str

    def load(self, data: dict):
        super().load(data)
        self.name = data.get('name', '')
        self.price = float(data.get('price', 0))
        self.image = data.get('image', '')

        return self
