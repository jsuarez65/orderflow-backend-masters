
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine('postgresql+psycopg2://ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech:5432/' + 
                        'orderflow?user=neondb_owner&password=npg_oYRmQ2e0IHaT&sslmode=require')

sessionLocal = sessionmaker(bind=engine)
