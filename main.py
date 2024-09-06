import os
from typing import Optional, List
from fastapi import FastAPI, Path, Request, HTTPException, Depends #Path para validar queryparams
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from config.database import engine, Base, Session
from models.movie import Movie

from auth import create_token
from auth import validate_token

load_dotenv() #carga variables de entorno

secretKey = os.getenv("SECRET_KEY")

app = FastAPI()
app.title = 'Movies WebAPI ⚡️'
app.version = "1.0.0"
ROUTER = 'api'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials, secretKey)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credentiales invalidas")

class MovieMetaObj(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
                }
            }


class User(BaseModel):
    email: str
    password: str


movies = [
    {
    "id": 2,
    "title": "Mundo",
    "category": "scared"
    },
    {
    "id": 2,
    "title": "Mundo",
    "category": "funny"
    }
]

# Authentica tu usuario

@app.post('/auth/login', tags=['Auth'])
def login (user: User):
    if user.email == "admin@gmail.com" and user.password == "1015186487":
        token: str = create_token(user.dict(), secretKey)

    return JSONResponse(content=token, status_code=200)


# obten todas las peliculas

@app.get('/movies', tags=['Movies'], response_model=List[MovieMetaObj], status_code=200, dependencies=[Depends(JWTBearer)]) #Indicar a la funcion que voy a devolver una lista
def get_movies():
    return JSONResponse(content=movies)

# obten una pelicula por el ID

@app.get('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def get_moview_id(id: int = Path(ge=1, le=2000)): # Parametros de busqueda
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)

    return JSONResponse(content=[], status_code=404)


# obten peliculas por parametros

@app.get('/movies/', tags=['Movies'], response_model=List[MovieMetaObj], status_code=200)
def get_movies_by_categories(category: str): # Parametro query
    for items in movies:
        if items["category"] == category:
            return JSONResponse(content=items)

    return JSONResponse(content=[], status_code=404)


# Postea nuevas peliculas

@app.post('/movies', tags=["Movies"], response_model=dict, status_code=201)
def post_movies(movie: MovieMetaObj) -> dict:
    db = Session()
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Pelicula correctamente creada"})


# Modificar peliculas

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie (id: int, movie: MovieMetaObj):
    for item in movies:
        if item["id"] == id:
		        item['title'] = movie.title
		        item['category'] = movie.category

        return JSONResponse(content={"message": "Pelicula correctamente creada"})


# Eliminar peliculas

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Pelicula correctamente creada"})
