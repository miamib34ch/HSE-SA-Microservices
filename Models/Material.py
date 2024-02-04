from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def material_from_dict(s: Any) -> Material:
    return Material.from_dict(s)


def material_to_dict(x: Material) -> Any:
    return to_class(Material, x)