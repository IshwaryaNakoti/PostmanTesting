from pydantic import BaseModel
import json

class Nutrition(BaseModel):
    calories: int
    sugar: str
    fiber: str

class Fruits(BaseModel):
    name: str
    color: str
    season: str
    nutrition: Nutrition