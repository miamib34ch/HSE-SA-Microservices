from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast
from Models.Route import Route


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class User:
    token: str
    user_id: int
    username: str
    is_tourist: bool
    created_routes: List[Route]

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        token = from_str(obj.get("token"))
        user_id = from_int(obj.get("user_id"))
        username = from_str(obj.get("username"))
        is_tourist = from_bool(obj.get("is_tourist"))
        created_routes = from_list(lambda x: x, obj.get("created_routes"))
        return User(token, user_id, username, is_tourist, created_routes)

    def to_dict(self) -> dict:
        result: dict = {"token": from_str(self.token), "user_id": from_int(self.user_id),
                        "username": from_str(self.username), "is_tourist": from_bool(self.is_tourist),
                        "created_routes": from_list(lambda x: x, self.created_routes)}
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)


@dataclass
class NewUser:
    username: str
    is_tourist: bool
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'NewUser':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        is_tourist = from_bool(obj.get("is_tourist"))
        password = from_str(obj.get("password"))
        return NewUser(username, is_tourist, password)

    def to_dict(self) -> dict:
        result: dict = {"username": from_str(self.username), "is_tourist": from_bool(self.is_tourist),
                        "password": from_str(self.password)}
        return result


def new_user_from_dict(s: Any) -> NewUser:
    return NewUser.from_dict(s)


def new_user_to_dict(x: NewUser) -> Any:
    return to_class(NewUser, x)


@dataclass
class EditUser:
    username: str | None = None
    is_tourist: bool | None = None
    password: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditUser':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        is_tourist = from_bool(obj.get("is_tourist"))
        password = from_str(obj.get("password"))
        return EditUser(username, is_tourist, password)

    def to_dict(self) -> dict:
        result: dict = {"username": from_str(self.username), "is_tourist": from_bool(self.is_tourist),
                        "password": from_str(self.password)}
        return result


def edit_user_from_dict(s: Any) -> EditUser:
    return EditUser.from_dict(s)


def edit_user_to_dict(x: EditUser) -> Any:
    return to_class(EditUser, x)
