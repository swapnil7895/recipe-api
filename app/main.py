from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title = "Personal Recip and Meal Planner API",
    description = "A beginnner friendly API to manage your favourite cooking recipies.",
    version = "1.0.0"
)

RECIPES = {
    1: {
        "id": 1,
        "title": "Classic Margherita Pizza",
        "description": "Simple and delicious Italian pizza with fresh mozzarella and basil.",
        "cooking_time_minutes": 25,
        "instructions": "Roll dough, add sauce and cheese, bake at 450°F for 12 minutes."
        }
}

recipe_id_counter = 2

class RecipeCreate(BaseModel):
    title: str = Field(...,min_length=1, max_length=100, example="Spaghetti Carbonara")
    description: Optional[str] = Field(None, max_length=300,example="Classic roman pasta dish" )
    cooking_time_minutes: int = Field(...,gt=0,example=20)
    instructions: str = Field(...,min_length=10,example="Boil pasta, fry guanciale, mix egg and cheese off-heat.")

class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    cooking_time_minutes: int
    instructions: str



@app.get("/")
def get_root():
    return {"message": "this is root endpoint"}    

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def get_recipe(recipe_id: int):
    if recipe_id not in RECIPES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Recipe with ID {recipe_id} not found"
        )
    return RECIPES[recipe_id]

@app.get("/recipes", response_model=List[RecipeResponse], status_code=status.HTTP_200_OK)
def get_recipes(search: Optional[str]=None, limit=10):
    results = list(RECIPES.values())

    if search:
        results = [r for r in results  if search.lower() in r["title"].lower() ]

    return results[:limit]

@app.post("/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_data: RecipeCreate):
    global recipe_id_counter
    new_recipe = recipe_data.model_dump()
    new_recipe["id"] = recipe_id_counter
    RECIPES[recipe_id_counter]= new_recipe
    recipe_id_counter +=1

    return new_recipe

@app.put("/recipes/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def update_recipe(recipe_id: int, updated_data: RecipeCreate):
    if recipe_id not in RECIPES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with {id} not found."
        )    

    stored_recipe = updated_data.model_dump()
    stored_recipe["id"] = recipe_id
    RECIPES[recipe_id] = stored_recipe
    return stored_recipe


@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int):
    if recipe_id not in RECIPES:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUN,
            detail = f"Recipe with ID {recipe_id} not found"
        )
    del RECIPES[recipe_id]
    return None
    