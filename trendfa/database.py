from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from trendfa.models import Base

import settings

# CONNECTION_STRING = 'sqlite:///trendfa.db'
CONNECTION_STRING = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
    user=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
)

engine = create_engine(CONNECTION_STRING)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()
