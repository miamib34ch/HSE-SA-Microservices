from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
import httpx
import os

from app.Models.User import User, NewUser, EditUser
from app.Models.Route import Route, NewRoute, EditRoute
from app.Models.Waypoint import Waypoint, NewWaypoint, EditWaypoint


app = FastAPI()
bearer_scheme = HTTPBearer()

USER_SERVICE_URL = str(os.environ.get('USER_SERVICE_URL')) + "/user/"
ROUTE_URL = str(os.environ.get('ROUTE_URL')) + "/route/"
POINT_URL = str(os.environ.get('POINT_URL ')) + "/point/"


@app.post("/user/", response_model=User, status_code=201)
async def create_user(new_user: NewUser):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}", json=new_user.to_dict())

        if response.status_code == 409:
            raise HTTPException(status_code=409,
                                detail="Конфликт пользователь с таким именем уже существует")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.get("/user/{user_id}", response_model=User, status_code=200)
async def read_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}{user_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Пользователь с указанным user_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.put("/user/{user_id}", response_model=User, status_code=200)
async def update_user(user_id: int, edit_user: EditUser):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{USER_SERVICE_URL}{user_id}", json=edit_user.to_dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Пользователь с указанным user_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.delete("/user/{user_id}", response_model={}, status_code=204)
async def delete_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SERVICE_URL}{user_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Пользователь с указанным user_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return {}


# Route
@app.post("/route/", response_model=Route, status_code=201)
async def create_route(new_route: NewRoute):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ROUTE_URL}", json=new_route.to_dict())

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.get("/route/{route_id}", response_model=Route, status_code=200)
async def read_route(route_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ROUTE_URL}{route_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Маршрут с указанным route_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.put("/route/{route_id}", response_model=Route, status_code=200)
async def update_route(route_id: int, edit_route: EditRoute):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{ROUTE_URL}{route_id}", json=edit_route.to_dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Маршрут с указанным route_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.delete("/route/{route_id}", response_model={}, status_code=204)
async def delete_route(route_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{ROUTE_URL}{route_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Маршрут с указанным route_id не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return {}


# Waypoint
@app.post("/point/", response_model=Waypoint, status_code=201)
async def create_point(new_point: NewWaypoint):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{POINT_URL}", json=new_point.to_dict())

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.get("/point/{point_id}", response_model=Waypoint, status_code=200)
async def read_point(point_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POINT_URL}{point_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Точка интереса с указанным point_id не найдена")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.put("/point/{point_id}", response_model=Waypoint, status_code=200)
async def update_point(point_id: int, edit_point: EditWaypoint):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{POINT_URL}{point_id}", json=edit_point.to_dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Точка интереса с указанным point_id не найдена")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return response.json()


@app.delete("/point/{point_id}", response_model={}, status_code=204)
async def delete_point(point_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{POINT_URL}{point_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Точка интереса с указанным point_id не найдена")

        if response.status_code == 422:
            raise HTTPException(status_code=422,
                                detail="Некорректный запрос (например, отсутствие обязательных параметров)")

        return {}
