from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from app.Models.Waypoint import NewWaypoint, Waypoint


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Route:
    route_id: int
    name: str
    description: str
    waypoints: List[Waypoint]

    @staticmethod
    def from_dict(obj: Any) -> 'Route':
        assert isinstance(obj, dict)
        route_id = from_int(obj.get("route_id"))
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        waypoints = from_list(Waypoint.from_dict, obj.get("waypoints"))
        return Route(route_id, name, description, waypoints)

    def to_dict(self) -> dict:
        result: dict = {"route_id": from_int(self.route_id), "name": from_str(self.name),
                        "description": from_str(self.description),
                        "waypoints": from_list(lambda x: to_class(Waypoint, x), self.waypoints)}
        return result


def route_from_dict(s: Any) -> Route:
    return Route.from_dict(s)


def route_to_dict(x: Route) -> Any:
    return to_class(Route, x)


@dataclass
class NewRoute:
    name: str
    description: str
    waypoints: List[NewWaypoint]

    @staticmethod
    def from_dict(obj: Any) -> 'NewRoute':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        waypoints = from_list(NewWaypoint.from_dict, obj.get("waypoints"))
        return NewRoute(name, description, waypoints)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "description": from_str(self.description),
                        "waypoints": from_list(lambda x: to_class(NewWaypoint, x), self.waypoints)}
        return result


def new_route_from_dict(s: Any) -> NewRoute:
    return NewRoute.from_dict(s)


def new_route_to_dict(x: NewRoute) -> Any:
    return to_class(NewRoute, x)


@dataclass
class EditRoute:
    name: str | None = None
    description: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditRoute':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        return EditRoute(name, description)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "description": from_str(self.description)}
        return result


def edit_route_from_dict(s: Any) -> EditRoute:
    return EditRoute.from_dict(s)


def edit_route_to_dict(x: EditRoute) -> Any:
    return to_class(EditRoute, x)
