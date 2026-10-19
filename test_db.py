from app.database import engine
from sqlalchemy import text

with engine.connect() as connections:
    result = connections.execute(text("Select 1"))
    print(result.scalar())
