import pytest
from app.user_service import create_user, read_user, update_user, delete_user
from app.Models.User import NewUser, User, EditUser


# Последовательность тестов обязательна
@pytest.mark.asyncio
async def test_create_user():
    user_name = "test_user123"
    new_user = NewUser(username=user_name,
                       is_tourist=True,
                       password="test_password")
    created_user = await create_user(new_user=new_user)
    assert created_user.username is user_name


@pytest.mark.asyncio
async def test_read_user():
    user = await read_user(user_id=1)
    assert user is not None


@pytest.mark.asyncio
async def test_update_user():
    edit_name = "test5444"
    edit_user = EditUser(username=edit_name,
                         is_tourist=True,
                         password="test_password")
    created_user = await update_user(user_id=1,
                                     edit_user=edit_user)
    assert created_user.username is edit_name


@pytest.mark.asyncio
async def test_delete_user():
    user = await delete_user(user_id=1)
    assert user is not None


@pytest.mark.asyncio
async def test_delete_failure_user():
    try:
        await delete_user(user_id=1)
        pytest.fail("User deleted")
    except:
        pass


@pytest.mark.asyncio
async def test_update_failure_user():
    try:
        edit_name = "test5444"
        edit_user = EditUser(username=edit_name,
                             is_tourist=True,
                             password="test_password")
        await update_user(user_id=1,
                          edit_user=edit_user)
        pytest.fail("User updated")
    except:
        pass


@pytest.mark.asyncio
async def test_read_failure_user():
    try:
        await read_user(user_id=1)
        pytest.fail("User readed")
    except:
        pass
