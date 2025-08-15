from __future__ import annotations

from typing import Optional, Any, List
from sqlalchemy.exc import IntegrityError

from backend.src.worktracker.repositories.ports import TaskRepositoryPort, UserRepositoryPort
from backend.src.worktracker.schemas.task import TaskCreate, TaskRead, TaskUpdate




class NotFoundError(Exception):
    """Kaynak (task) bulunamadığında servis katmanının fırlattığı domain hatası."""
    pass


class AssigneeNotFoundError(Exception):
    """Verilen assignee_id geçerli bir kullanıcıya ait değil."""
    pass


class TaskService:
    """
    Task iş kuralları + mapping + (opsiyonel) WS publish.
    - assignee doğrulaması servis katmanında yapılır.
    - ws_publisher; WebSocketHub benzeri bir nesne olmalı.
      Beklenen imzalar (senin tasarımına göre):
        ws.publish_task_created(task_id: int, assignee_id: int | None) -> None
        ws.publish_task_updated(task_id: int) -> None
    """

    def __init__(
        self,
        task_repo: TaskRepositoryPort,
        user_repo: UserRepositoryPort,
        *,
        ws_publisher: Optional[Any] = None,
    ) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.ws = ws_publisher

    # -------- helpers --------
    def _norm_str(self, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        s = v.strip()
        return s or None

    def _ensure_assignee_exists(self, assignee_id: Optional[int]) -> None:
        if assignee_id is None:
            return
        if self.user_repo.get_by_id(assignee_id) is None:
            raise AssigneeNotFoundError("Assignee user not found")

    # -------- API (ports) --------
    def create(self, data: TaskCreate) -> TaskRead:
        # Temizlik
        title = self._norm_str(data.title) or ""  # title zorunlu
        description = self._norm_str(data.description)
        status = data.status  # Pydantic Enum doğrulaması zaten yapıldı
        assignee_id = data.assignee_id

        # İş kuralı: assignee var mı?
        self._ensure_assignee_exists(assignee_id)

        try:
            task = self.task_repo.create(
                title=title,
                description=description,
                status=status,
                assignee_id=assignee_id,
            )
        except IntegrityError as e:
            # FK ihlali vb. durumlar teorik olarak buraya düşebilir
            raise AssigneeNotFoundError("Assignee user not found") from e

        # WS publish (async tetiklemeyi hub içinde hallediyoruz)
        if self.ws:
            try:
                self.ws.publish_task_created(task.id, assignee_id=task.assignee_id)
            except Exception:
                # Event yayınında hata olsa bile ana akışı bozmayalım
                pass

        return TaskRead.model_validate(task, from_attributes=True)

    def get(self, task_id: int) -> TaskRead:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return TaskRead.model_validate(task, from_attributes=True)

    def list(self) -> List[TaskRead]:
        tasks = self.task_repo.list()
        return [TaskRead.model_validate(t, from_attributes=True) for t in tasks]

    def update(self, task_id: int, data: TaskUpdate) -> TaskRead:
        # assignee_id alanı gönderildiyse validasyon yap
        if data.assignee_id is not None:
            # None gönderilmişse (assignee kaldırma) validasyona gerek yok
            if data.assignee_id is not None:
                self._ensure_assignee_exists(data.assignee_id)

        try:
            task = self.task_repo.update(
                task_id,
                title=self._norm_str(data.title) if data.title is not None else None,
                description=self._norm_str(data.description) if data.description is not None else None,
                status=data.status,
                assignee_id=data.assignee_id,  # kaldırmak için None gelebilir
            )
        except ValueError:
            # repo "bulunamadı"yı ValueError ile bildiriyor
            raise NotFoundError("Task not found")
        except IntegrityError as e:
            raise AssigneeNotFoundError("Assignee user not found") from e

        if self.ws:
            try:
                self.ws.publish_task_updated(task.id)
            except Exception:
                pass

        return TaskRead.model_validate(task, from_attributes=True)
