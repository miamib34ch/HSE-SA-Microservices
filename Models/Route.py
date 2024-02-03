from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Material:
    material_id: int
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'Material':
        assert isinstance(obj, dict)
        material_id = from_int(obj.get("material_id"))
        title = from_str(obj.get("title"))
        return Material(material_id, title)

    def to_dict(self) -> dict:
        result: dict = {"material_id": from_int(self.material_id), "title": from_str(self.title)}
        return result


@dataclass
class Waypoint:
    latitude: float
    longitude: float
    description: str
    materials: List[Material]

    @staticmethod
    def from_dict(obj: Any) -> 'Waypoint':
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        description = from_str(obj.get("description"))
        materials = from_list(Material.from_dict, obj.get("materials"))
        return Waypoint(latitude, longitude, description, materials)

    def to_dict(self) -> dict:
        result: dict = {"latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "description": from_str(self.description),
                        "materials": from_list(lambda x: to_class(Material, x), self.materials)}
        return result


@dataclass
class Route:
    name: str
    description: str
    waypoints: List[Waypoint]

    @staticmethod
    def from_dict(obj: Any) -> 'Route':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        waypoints = from_list(Waypoint.from_dict, obj.get("waypoints"))
        return Route(name, description, waypoints)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "description": from_str(self.description),
                        "waypoints": from_list(lambda x: to_class(Waypoint, x), self.waypoints)}
        return result


def route_from_dict(s: Any) -> Route:
    return Route.from_dict(s)


def route_to_dict(x: Route) -> Any:
    return to_class(Route, x)
