from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from Models.User import User, NewUser, EditUser
from Models.Route import Route, NewRoute, EditRoute
from Models.Waypoint import Waypoint, NewWaypoint, EditWaypoint
from Models.Material import Material

from Auth import generate_token

app = FastAPI()
bearer_scheme = HTTPBearer()

user_database = {}
routes_database = {}
points_database = {}
materials_database = {}


def find_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not any(user.token == token.credentials for user in user_database.values()):
        return False
    return True


# User
@app.post("/user/", response_model=User, status_code=201)
async def create_user(new_user: NewUser):
    if new_user.username in [u.username for u in user_database.values()]:
        raise HTTPException(status_code=409, detail="Конфликт пользователь с таким именем уже существует")

    if not new_user.username or not new_user.is_tourist or not new_user.password:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    user_id = len(user_database) + 1
    token = generate_token(new_user.password)

    user = User(token=token,
                user_id=user_id,
                username=new_user.username,
                is_tourist=new_user.is_tourist,
                created_routes=[])

    user_database[user_id] = user

    return user


@app.get("/user/{user_id}", response_model=User, status_code=200)
async def read_user(user_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if user_id not in user_database:
        raise HTTPException(status_code=404, detail="Пользователь с указанным user_id не найден")

    if not user_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return user_database[user_id]


@app.put("/user/{user_id}", response_model=User, status_code=200)
async def create_user(user_id: int, edit_user: EditUser, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if user_id not in user_database:
        raise HTTPException(status_code=404, detail="Пользователь с указанным user_id не найден")

    if not user_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    if edit_user.is_tourist is not None:
        user_database[user_id].is_tourist = edit_user.is_tourist
    if edit_user.username is not None:
        user_database[user_id].username = edit_user.username
    if edit_user.password is not None:
        user_database[user_id].password = edit_user.password

    return user_database[user_id]


@app.delete("/user/{user_id}", response_model={}, status_code=204)
async def create_user(user_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if user_id not in user_database:
        raise HTTPException(status_code=404, detail="Пользователь с указанным user_id не найден")

    if not user_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    user_database.pop(user_id)

    return {}


# Route
@app.post("/route/", response_model=Route, status_code=201)
async def create_route(new_route: NewRoute, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if not new_route.name or not new_route.description or not new_route.waypoints:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    route_id = len(routes_database) + 1
    route_points = []

    for new_waypoint in new_route.waypoints:
        waypoint_id = len(points_database) + 1
        route_waypoint_id = len(route_points) + 1
        points_database[waypoint_id] = Waypoint(point_id=waypoint_id,
                                                latitude=new_waypoint.latitude,
                                                longitude=new_waypoint.longitude,
                                                description=new_waypoint.description,
                                                materials=[])
        route_points.append(Waypoint(point_id=waypoint_id,
                                     latitude=new_waypoint.latitude,
                                     longitude=new_waypoint.longitude,
                                     description=new_waypoint.description,
                                     materials=[]))

    route = Route(
        route_id=route_id,
        name=new_route.name,
        description=new_route.description,
        waypoints=route_points
    )

    routes_database[route_id] = route

    return route


@app.get("/route/{route_id}", response_model=Route, status_code=200)
async def read_route(route_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if route_id not in routes_database:
        raise HTTPException(status_code=404, detail="Маршрут с указанным route_id не найден")

    if not route_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return routes_database[route_id]


@app.put("/route/{route_id}", response_model=Route, status_code=200)
async def update_route(route_id: int, edit_route: EditRoute, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if route_id not in routes_database:
        raise HTTPException(status_code=404, detail="Маршрут с указанным route_id не найден")

    if not route_id or not edit_route:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    if edit_route.name is not None:
        routes_database[route_id].name = edit_route.name
    if edit_route.description is not None:
        routes_database[route_id].description = edit_route.description

    return routes_database[route_id]


@app.delete("/route/{route_id}", response_model={}, status_code=204)
async def delete_route(route_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if route_id not in routes_database:
        raise HTTPException(status_code=404, detail="Маршрут с указанным route_id не найден")

    if not route_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    waypoint_ids = [waypoint.point_id for waypoint in routes_database[route_id].waypoints]

    routes_database.pop(route_id)

    for waypoint_id in waypoint_ids:
        points_database.pop(waypoint_id, None)

    return {}


# Waypoint
@app.post("/point/", response_model=Waypoint, status_code=201)
async def create_point(new_point: NewWaypoint, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if not new_point.latitude or not new_point.longitude or not new_point.description:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    point_id = len(points_database) + 1

    point = Waypoint(
        point_id=point_id,
        latitude=new_point.latitude,
        longitude=new_point.longitude,
        description=new_point.description,
        materials=[],
    )

    points_database[point_id] = point

    return point


@app.get("/point/{point_id}", response_model=Waypoint, status_code=200)
async def read_point(point_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if point_id not in points_database:
        raise HTTPException(status_code=404, detail="Точка интереса с указанным point_id не найдена")

    if not point_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return points_database[point_id]


@app.put("/point/{point_id}", response_model=Waypoint, status_code=200)
async def update_point(point_id: int, edit_point: EditWaypoint, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if point_id not in points_database:
        raise HTTPException(status_code=404, detail="Точка интереса с указанным point_id не найдена")

    if not point_id or not edit_point:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    if edit_point.latitude is not None:
        points_database[point_id].latitude = edit_point.latitude
    if edit_point.longitude is not None:
        points_database[point_id].longitude = edit_point.longitude
    if edit_point.description is not None:
        points_database[point_id].description = edit_point.description

    for route in routes_database.values():
        for waypoint in route.waypoints:
            if waypoint.point_id == point_id:
                if edit_point.latitude is not None:
                    waypoint.latitude = edit_point.latitude
                if edit_point.longitude is not None:
                    waypoint.longitude = edit_point.longitude
                if edit_point.description is not None:
                    waypoint.description = edit_point.description

    return points_database[point_id]


@app.delete("/point/{point_id}", response_model={}, status_code=204)
async def delete_point(point_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if point_id not in points_database:
        raise HTTPException(status_code=404, detail="Точка интереса с указанным point_id не найдена")

    if not point_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    points_database.pop(point_id)

    for route in routes_database.values():
        route.waypoints = [waypoint for waypoint in route.waypoints if waypoint.point_id != point_id]

    return {}


@app.post("/material/", response_model=Material, status_code=201)
async def create_material(file: UploadFile = File(...), our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if not file:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    material_id = len(materials_database) + 1

    material = Material(material_id=material_id, title=file.filename)
    materials_database[material_id] = material

    return material


@app.delete("/material/{material_id}", response_model={}, status_code=204)
async def delete_material(material_id: int, our_user: bool = Depends(find_user)):
    if not our_user:
        raise HTTPException(status_code=401, detail="Ошибка авторизации, отсутствует или неверный токен")

    if material_id not in materials_database:
        raise HTTPException(status_code=404, detail="Материал с указанным material_id не найден")

    if not material_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    materials_database.pop(material_id)

    return {}
