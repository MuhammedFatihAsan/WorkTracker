from __future__ import annotations

from typing import Optional, List
from sqlmodel import Session, select

from backend.src.worktracker.models.task import Task, TaskStatus
from backend.src.worktracker.repositories.ports import TaskRepositoryPort

class SQLModelTaskRepository(TaskRepositoryPort):
    """
    Task veri erişimi için SQLModel/PostgreSQL implementasyonu.
    - Sadece DB CRUD yapar.
    - commit/refresh ile kalıcı nesneyi döndürür.
    - Bulunamayan kayıtta update() ValueError atar (service 404'a çevirir).
    - FK/UNIQUE/NULL ihlallerinde IntegrityError doğal olarak fırlar (service map eder).
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        *,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        assignee_id: Optional[int] = None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            assignee_id=assignee_id,
        )
        self.session.add(task)
        self.session.commit()        # INSERT
        self.session.refresh(task)   # DB'nin son halini (id dahil) yükle
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def list(self) -> List[Task]:
        # Basit listeleme (ileride filtre/paginasyon eklenebilir)
        stmt = select(Task)  # istersen .order_by(Task.id.desc()) ekleyebilirsin
        return list(self.session.exec(stmt))

    def update(
        self,
        task_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        assignee_id: Optional[int] = None,
    ) -> Task:
        task = self.session.get(Task, task_id)
        if not task:
            raise ValueError("Task not found")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if assignee_id is not None:
            task.assignee_id = assignee_id

        self.session.add(task)
        self.session.commit()        # UPDATE
        self.session.refresh(task)
        return task
