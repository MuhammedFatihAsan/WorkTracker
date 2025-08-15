from typing import Optional
from pydantic import Field, constr
from sqlmodel import SQLModel

from backend.src.worktracker.models.task import TaskStatus

class TaskCreate(SQLModel):
    # title alanı:
    # - Field(pattern=...): Pydantic v2'de regex yerine pattern kullanılır
    # - Bu desen: yalnızca Türkçe/İngilizce harf ve boşluk (2–50 karakter)
    title: str = Field(pattern=r"^[A-Za-zÇĞİÖŞÜçğıöşü ]{2,50}$")
    # description alanı:
    # - constr: string için kısıtlı tip
    # - strip_whitespace=True: başındaki ve sonundaki boşlukları otomatik temizler
    # - min_length=1: temizlendikten sonra uzunluğu en az 1 karakter olmalı (boş bırakılamaz)
    # - | None: opsiyonel, yani değer gelmeyebilir
    # - = None: eğer gönderilmezse varsayılan olarak None atanır
    # - Bu yapı Optional[str] ile aynı opsiyonellik özelliğini taşır
    #   fakat string geldiğinde constr içindeki kurallar da uygulanır
    # - # type: ignore: tip kontrol aracının (ör. mypy) bu satırda uyarı vermesini engeller, zorunlu değil
    description: constr(strip_whitespace=True, min_length=1) | None = None # type: ignore
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None

class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    assignee_id: Optional[int] = None

class TaskUpdate(SQLModel):
    # title opsiyonel: gönderilirse biçim doğrulansın
    title: str | None = Field(default=None, pattern=r"^[A-Za-zÇĞİÖŞÜçğıöşü ]{2,50}$")
    # opsiyonel; gelirse boş olamaz (strip + min_length=1)
    description: constr(strip_whitespace=True, min_length=1) | None = None  # type: ignore
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
