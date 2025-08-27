from src.core.domain.exceptions.exceptions import NotAuthenticated


class TokenExpired(NotAuthenticated):
    detail = "Token has expired"


class IncorrectPassword(NotAuthenticated):
    detail = "Incorrect password"
