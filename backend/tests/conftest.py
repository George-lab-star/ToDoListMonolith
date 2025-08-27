import pytest

from tests.fakes.unit.users import FakeUserUnitOfWork
from tests.fakes.unit.tasks import FakeTaskUnitOfWork


@pytest.fixture
def fake_user_uow():
    return FakeUserUnitOfWork()


@pytest.fixture
def fake_password_hasher():
    return 'hashed_secure_pwd'


@pytest.fixture
def fake_task_uow():
    return FakeTaskUnitOfWork()
