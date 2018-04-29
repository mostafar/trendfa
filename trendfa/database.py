from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from trendfa.models import Base

from settings import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

# CONNECTION_STRING = 'sqlite:///trendfa.db'
CONNECTION_STRING = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
)

engine = create_engine(CONNECTION_STRING)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()
