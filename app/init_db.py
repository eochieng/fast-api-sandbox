from app.database import engine, Base
from app.models import User, Order


Base.metadata.create_all(bind=engine)
