from fastapi import FastAPI, HTTPException

from app.Models.Route import Route, NewRoute, EditRoute
from app.Models.Waypoint import Waypoint, NewWaypoint, EditWaypoint


app = FastAPI()

routes_database = {}
points_database = {}
materials_database = {}


# Route
@app.post("/route/", response_model=Route, status_code=201)
async def create_route(new_route: NewRoute):
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
async def read_route(route_id: int):
    if route_id not in routes_database:
        raise HTTPException(status_code=404, detail="Маршрут с указанным route_id не найден")

    if not route_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return routes_database[route_id]


@app.put("/route/{route_id}", response_model=Route, status_code=200)
async def update_route(route_id: int, edit_route: EditRoute):
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
async def delete_route(route_id: int):
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
async def create_point(new_point: NewWaypoint):
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
async def read_point(point_id: int):
    if point_id not in points_database:
        raise HTTPException(status_code=404, detail="Точка интереса с указанным point_id не найдена")

    if not point_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return points_database[point_id]


@app.put("/point/{point_id}", response_model=Waypoint, status_code=200)
async def update_point(point_id: int, edit_point: EditWaypoint):
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
async def delete_point(point_id: int):
    if point_id not in points_database:
        raise HTTPException(status_code=404, detail="Точка интереса с указанным point_id не найдена")

    if not point_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    points_database.pop(point_id)

    for route in routes_database.values():
        route.waypoints = [waypoint for waypoint in route.waypoints if waypoint.point_id != point_id]

    return {}
