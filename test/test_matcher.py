from user import User
from tradematcher.matcher import (
    read_users,
    write_users,
)
import pytest
from mock import MagicMock

@pytest.mark.skip("Need to finish off the mocking")
def test_read_users():
    cache = MagicMock()
    users = read_users(cache)
    assert [isinstance(user, User) for user in users]
    cache.get.assert_called
    

@pytest.mark.skip("Need to finish off the mocking")
def test_write_users():
    cache = MagicMock()
    users = [User()]
    write_users(cache, users)
    cache.set.assert_called()

