from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, Session, SQLModel

from tcgindex.models import (
    Game,
    Catalog,
    ProtoSet,
    SetRepresentation,
    ProtoCard,
    CardRepresentation,
)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    Path(sqlite_file_name).unlink()
    SQLModel.metadata.create_all(engine)


create_db_and_tables()
app = FastAPI()
