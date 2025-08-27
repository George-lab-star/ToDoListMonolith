from src.core.domain.exceptions.exceptions import AlreadyExists, NotFound


class TaskAlreadyExists(AlreadyExists):
    detail = "Task with this data already exists"


class TaskNotFound(NotFound):
    detail = "Task with this ID not found"
