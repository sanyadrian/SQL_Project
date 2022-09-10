from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite://')
conn = engine.connect()
Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()