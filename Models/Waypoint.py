from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from Models.Material import Material

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
class Waypoint:
    point_id: int
    latitude: float
    longitude: float
    description: str
    materials: List[Material]

    @staticmethod
    def from_dict(obj: Any) -> 'Waypoint':
        assert isinstance(obj, dict)
        point_id = from_int(obj.get("point_id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        description = from_str(obj.get("description"))
        materials = from_list(Material.from_dict, obj.get("materials"))
        return Waypoint(point_id, latitude, longitude, description, materials)

    def to_dict(self) -> dict:
        result: dict = {"point_id": from_int(self.point_id), "latitude": to_float(self.latitude),
                        "longitude": to_float(self.longitude), "description": from_str(self.description),
                        "materials": from_list(lambda x: to_class(Material, x), self.materials)}
        return result


def waypoint_from_dict(s: Any) -> Waypoint:
    return Waypoint.from_dict(s)


def waypoint_to_dict(x: Waypoint) -> Any:
    return to_class(Waypoint, x)


@dataclass
class NewWaypoint:
    latitude: float
    longitude: float
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'NewWaypoint':
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        description = from_str(obj.get("description"))
        return NewWaypoint(latitude, longitude, description)

    def to_dict(self) -> dict:
        result: dict = {"latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "description": from_str(self.description)}
        return result


def new_waypoint_from_dict(s: Any) -> NewWaypoint:
    return NewWaypoint.from_dict(s)


def new_waypoint_to_dict(x: NewWaypoint) -> Any:
    return to_class(NewWaypoint, x)


@dataclass
class EditWaypoint:
    latitude: float | None = None
    longitude: float | None = None
    description: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditWaypoint':
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        description = from_str(obj.get("description"))
        return EditWaypoint(latitude, longitude, description)

    def to_dict(self) -> dict:
        result: dict = {"latitude": to_float(self.latitude), "longitude": to_float(self.longitude),
                        "description": from_str(self.description)}
        return result


def edit_waypoint_from_dict(s: Any) -> EditWaypoint:
    return EditWaypoint.from_dict(s)


def edit_waypoint_to_dict(x: EditWaypoint) -> Any:
    return to_class(EditWaypoint, x)