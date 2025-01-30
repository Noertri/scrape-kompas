from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.dialects.sqlite import TEXT, INTEGER


class Base(DeclarativeBase):
    pass


class ArticlesDB(Base):
    __tablename__ = "artikel"
    rowid = mapped_column("id", INTEGER, primary_key=True, autoincrement=True)
    tanggal = mapped_column("tanggal", TEXT)
    judul = mapped_column("judul", TEXT)
    narasi = mapped_column("narasi", TEXT)
    url = mapped_column("url", TEXT, unique=True)
