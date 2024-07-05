from sqlalchemy import create_engine, URL
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import scoped_session, sessionmaker

url_object = URL.create(
    "mysql+pymysql",
    username='root',
    password='',
    host='localhost',
    port=3306,
    database='test',
)

engine = create_engine(
    url=url_object,
    echo=True,
    echo_pool='debug',
    pool_pre_ping=True,
    poolclass=StaticPool
)

def get_engine():
    return engine

def get_session(sa_engine):
    return scoped_session(
        sessionmaker(
            bind=sa_engine,
            expire_on_commit=False,
            autoflush=False
        )
    )