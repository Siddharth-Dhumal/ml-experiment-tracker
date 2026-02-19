from .base import Base
from .session import engine
from . import models

def init_db() -> None:
    Base.metadata.create_all(bind=engine)