from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.conf import settings

engine = create_engine(settings.DB_CONFIG, future=True, echo=True)

Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
