import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from ext import data_path


def create_db():
    url = "sqlite:///{0}".format(data_path.joinpath("artikel.sqlite3"))
    engine = create_engine(url)
    if not sa.inspect(engine).has_table("artikel"):
        Base.metadata.create_all(engine, checkfirst=True)
    return sessionmaker(engine)


if __name__ == "__main__":
    create_db()
