from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from tests.fakes.integration.pgtest_uow import TestPGTaskUnitOfWork


def get_test_task_uow() -> ITaskUnitOfWork:
    """
    Dependency that provides a test instance of IUserUnitOfWork.

    This allows the presentation layer to remain decoupled from the actual implementation.
    By default, it returns a PostgreSQL-based unit of work (PGUserUnitOfWork), but the implementation
    can be easily overridden for testing or different environments.

    :return: IUserUnitOfWork instance.
    """
    return TestPGTaskUnitOfWork()
