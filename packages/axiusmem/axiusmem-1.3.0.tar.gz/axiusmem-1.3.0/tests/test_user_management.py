import rdflib
import pytest
from axiusmem.user_management import UserManager

@pytest.fixture
def user_manager():
    g = rdflib.Graph()
    return UserManager(g)

def test_create_and_authenticate_user(user_manager):
    user_manager.create_user("alice", "password123", roles=["agent"])
    assert user_manager.authenticate_user("alice", "password123")
    assert not user_manager.authenticate_user("alice", "wrongpass")
    assert user_manager.is_agent("alice")
    assert not user_manager.is_admin("alice")

def test_assign_role(user_manager):
    user_manager.create_user("bob", "pw", roles=["agent"])
    user_manager.assign_role("bob", "admin")
    assert user_manager.is_admin("bob")
    roles = user_manager.get_user_roles("bob")
    assert set(roles) == {"agent", "admin"}

def test_duplicate_user(user_manager):
    user_manager.create_user("carol", "pw")
    with pytest.raises(ValueError):
        user_manager.create_user("carol", "pw")

def test_list_and_delete_users(user_manager):
    user_manager.create_user("dave", "pw")
    user_manager.create_user("eve", "pw")
    users = user_manager.list_users()
    assert set(users) == {"dave", "eve"}
    user_manager.delete_user("dave")
    assert user_manager.list_users() == ["eve"] 