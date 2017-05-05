from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DOCKER_HOST = 'mysql'

# CONNECTION_STRING = 'sqlite:///trendfa.db'
CONNECTION_STRING = 'mysql+pymysql://root:password@{}/trendfa'.format(DOCKER_HOST)

engine = create_engine(CONNECTION_STRING)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()
