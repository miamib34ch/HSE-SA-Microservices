from fastapi import FastAPI, HTTPException

from app.Models.User import User, NewUser, EditUser
from app.security import generate_token


app = FastAPI()

user_database = {}


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
async def read_user(user_id: int):
    if user_id not in user_database:
        raise HTTPException(status_code=404, detail="Пользователь с указанным user_id не найден")

    if not user_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    return user_database[user_id]


@app.put("/user/{user_id}", response_model=User, status_code=200)
async def create_user(user_id: int, edit_user: EditUser):
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
async def create_user(user_id: int):
    if user_id not in user_database:
        raise HTTPException(status_code=404, detail="Пользователь с указанным user_id не найден")

    if not user_id:
        raise HTTPException(status_code=422,
                            detail="Некорректный запрос (например, отсутствие обязательных параметров)")

    user_database.pop(user_id)

    return {}