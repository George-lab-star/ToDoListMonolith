from src.tasks.domain.entities import Task, TaskCreate, TaskUpdate
from src.tasks.domain.exceptions import TaskNotFound
from src.tasks.domain.interfaces.task_repo import ITaskRepo
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


class FakeTaskRepo(ITaskRepo):
    """
    In-memory implementation of ITaskRepo for testing purposes.
    Simulates task repository behavior without database persistence.
    """
    
    def __init__(self):
        """Initialize with empty task list and starting ID counter."""
        self._tasks = []
        self._last_task_id = 0

    async def add(self, task: TaskCreate, user_uow=IUserUnitOfWork) -> Task:
        """
        Add a new task to the repository.
        
        Args:
            task: TaskCreate object containing task data
            user_uow: User unit of work (unused in this implementation)
            
        Returns:
            Task: The newly created task with assigned ID
        """
        new_task = Task(id=self._get_new_task_id(), **task.dict,)
        self._tasks.append(new_task)
        return new_task

    async def get_by_id(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task: The found task
            
        Raises:
            TaskNotFound: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(detail=f"Task with id {task_id} not found")

    async def update(self, task: TaskUpdate) -> Task:
        """
        Update an existing task with new data.
        
        Args:
            task: TaskUpdate object containing fields to update
            
        Returns:
            Task: The updated task
        """
        updated_task = await self.get_by_id(task.id)
        for field, value in task.dict.items():
            if value is not None:
                setattr(updated_task, field, value)
        return updated_task

    async def delete(self, task_id: int) -> None:
        """
        Delete a task by its ID.
        
        Args:
            task_id: ID of the task to delete
            
        Raises:
            TaskNotFound: If no task with the given ID exists
        """
        task = await self.get_by_id(task_id)
        self._tasks.remove(task)

    async def list_tasks(self):
        """
        Retrieve all tasks in the repository.
        
        Returns:
            List[Task]: All stored tasks
        """
        return self._tasks

    def _get_new_task_id(self) -> int:
        """
        Generate a new unique task ID.
        
        Returns:
            int: The next available task ID
        """
        self._last_task_id += 1
        return self._last_task_id


class FakeTaskUnitOfWork(ITaskUnitOfWork):
    """
    In-memory implementation of ITaskUnitOfWork for testing.
    Manages transaction state for task operations.
    """
    
    tasks: ITaskRepo

    def __init__(self):
        """Initialize with task repository and commit state."""
        self.tasks = FakeTaskRepo()
        self.committed = False

    async def _commit(self):
        """
        Mark the current transaction as committed.
        Sets the committed flag to True.
        """
        self.committed = True

    async def rollback(self):
        """
        Rollback the current transaction.
        No-op in this in-memory implementation.
        """
        pass
