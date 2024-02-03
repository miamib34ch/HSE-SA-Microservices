from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class User:
    token: str
    user_id: int
    username: str
    email: str

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        token = from_str(obj.get("token"))
        user_id = from_int(obj.get("user_id"))
        username = from_str(obj.get("username"))
        email = from_str(obj.get("email"))
        return User(token, user_id, username, email)

    def to_dict(self) -> dict:
        result: dict = {"token": from_str(self.token), "user_id": from_int(self.user_id),
                        "username": from_str(self.username), "email": from_str(self.email)}
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)


@dataclass
class NewUser:
    username: str
    email: str
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'NewUser':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        email = from_str(obj.get("email"))
        password = from_str(obj.get("password"))
        return NewUser(username, email, password)

    def to_dict(self) -> dict:
        result: dict = {"username": from_str(self.username), "email": from_str(self.email),
                        "password": from_str(self.password)}
        return result


def new_user_from_dict(s: Any) -> NewUser:
    return NewUser.from_dict(s)


def new_user_to_dict(x: NewUser) -> Any:
    return to_class(NewUser, x)


@dataclass
class EditUser:
    username: str | None = None
    email: str | None = None
    password: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditUser':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        email = from_str(obj.get("email"))
        password = from_str(obj.get("password"))
        return EditUser(username, email, password)

    def to_dict(self) -> dict:
        result: dict = {"username": from_str(self.username), "email": from_str(self.email),
                        "password": from_str(self.password)}
        return result


def edit_user_from_dict(s: Any) -> EditUser:
    return EditUser.from_dict(s)


def edit_user_to_dict(x: EditUser) -> Any:
    return to_class(EditUser, x)
