from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ...models import Task, TaskStatus            # ORM model ve Enum
from ...schemas.task import TaskCreate, TaskRead, TaskUpdate  # DTO/şemalar
from ..deps import get_db

# /tasks altındaki uçları toplar
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskRead, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    """
    Yeni task oluşturur.
    - data.status gelmemişse varsayılanı TaskStatus.TODO kullanılır.
    - assignee_id opsiyoneldir; None ise görev kime atanacağı olmadan kaydedilir.
    """
    task = Task(
        title=data.title,
        description=data.description,
        status=data.status or TaskStatus.TODO,  # None ise TODO
        assignee_id=data.assignee_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task, from_attributes=True)

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    ID'ye göre tek task getirir.
    - Yoksa 404 döner.
    """
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return TaskRead.model_validate(task, from_attributes=True)

@router.get("", response_model=List[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    """
    Tüm task'ları listele.
    - SQLModel'de select(Task) + db.exec() ile sorgu çalıştırırız.
    - .all() → liste döner, sonra her birini TaskRead'e dönüştürürüz.
    """
    tasks = db.exec(select(Task)).all()
    return [TaskRead.model_validate(t, from_attributes=True) for t in tasks]

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Task için kısmi güncelleme.
    - Gönderilen alanlara göre title/description/status/assignee_id güncellenir.
    - TODO / IN_PROGRESS / DONE
    - Yoksa 404.
    """
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    # Kısmi güncelleme
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status
    if data.assignee_id is not None:
        task.assignee_id = data.assignee_id

    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task, from_attributes=True)
