from app.database import Base, engine
from app.models.task import Task
from app.models.user import User

Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
