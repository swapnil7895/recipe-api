from re import search
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.database import get_db
from app.models.recipe import Recipe as RecipeModel
from app.schemas.recipe import RecipeCreate, RecipeResponse


app = FastAPI(
    title = "Personal Recip and Meal Planner API",
    description = "A beginnner friendly API to manage your favourite cooking recipies.",
    version = "1.0.0"
)

# RECIPES = {
#     1: {
#         "id": 1,
#         "title": "Classic Margherita Pizza",
#         "description": "Simple and delicious Italian pizza with fresh mozzarella and basil.",
#         "cooking_time_minutes": 25,
#         "instructions": "Roll dough, add sauce and cheese, bake at 450°F for 12 minutes."
#         }
# }

# recipe_id_counter = 2

# class RecipeCreate(BaseModel):
#     title: str = Field(...,min_length=1, max_length=100, example="Spaghetti Carbonara")
#     description: Optional[str] = Field(None, max_length=300,example="Classic roman pasta dish" )
#     cooking_time_minutes: int = Field(...,gt=0,example=20)
#     instructions: str = Field(...,min_length=10,example="Boil pasta, fry guanciale, mix egg and cheese off-heat.")

# class RecipeResponse(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     cooking_time_minutes: int
#     instructions: str



# @app.get("/")
# def get_root():
#     return {"message": "this is root endpoint"}    

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def get_recipe(recipe_id: int, db: Session = Depends(get_db) ):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id ).first()

    if not db_recipe:
        raise HTTPException(status_code = 404, detail= "Recipe not found" )
    return db_recipe

@app.get("/recipes", response_model=List[RecipeResponse], status_code=status.HTTP_200_OK)
def get_recipes(search: Optional[str]=None, limit: int=10, db: Session = Depends(get_db) ):
    query = db.query(RecipeModel)
 
    if search:
        query = query.filter(
            (RecipeModel.title.icontains(search)) |
            (RecipeModel.description.icontains(search))
        )
    return query.limit(limit).all()

@app.post("/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_in: RecipeCreate, db: Session = Depends(get_db) ):
    db_recipe = RecipeModel(**recipe_in.model_dump() )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.put("/recipes/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def update_recipe(recipe_id: int, recipe_in: RecipeCreate, db: Session= Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code = 404, detail = "Recipe not found")
    for key, value in recipe_in.model_dump().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe



@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail = "Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return None
