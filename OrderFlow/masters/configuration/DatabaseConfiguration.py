
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine("postgresql://neondb_owner:npg_oYRmQ2e0IHaT@ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech/orderflow",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,)
SessionLocal = sessionmaker(bind=engine)