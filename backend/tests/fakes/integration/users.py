from src.users.domain.interfaces.user_uow import IUserUnitOfWork
from tests.fakes.integration.pgtest_uow import TestPGUserUnitOfWork

def get_test_user_uow() -> IUserUnitOfWork:
    """
    Dependency that provides a test instance of IUserUnitOfWork.

    This allows the presentation layer to remain decoupled from the actual implementation.
    By default, it returns a PostgreSQL-based unit of work (PGUserUnitOfWork), but the implementation
    can be easily overridden for testing or different environments.

    :return: IUserUnitOfWork instance.
    """
    return TestPGUserUnitOfWork()
