# Bu dosya, router modüllerini dışarı "kısa adlarla" açmak için var.
# main.py içinde:
#   from .api.routers import users_router, tasks_router
# diyerek import etmeyi kolaylaştırır.

from .users import router as users_router
from .tasks import router as tasks_router
