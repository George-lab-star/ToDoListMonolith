from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository
from tests.fakes.integration.pgtest_uow import TestRedisRefreshTokenRepository


def get_test_refresh_token_repository() -> IRefreshTokenRepository:

    return TestRedisRefreshTokenRepository()
