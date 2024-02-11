import pytest
from app.user_service import create_user, read_user
from app.Models.User import NewUser


@pytest.mark.asyncio
def test_create_user():
    new_user = NewUser(username="test_user",
                       is_tourist=True,
                       password="test_password")
    created_user = create_user(new_user)
    assert created_user is not None
