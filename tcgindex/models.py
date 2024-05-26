import datetime

from sqlalchemy import DateTime, func, text
from sqlmodel import Column, Field, SQLModel

class TimestampModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )

class Catalog(TimestampModel, table=True):
    ...

class Game(TimestampModel, table=True):
    name: str
    ...

class Expansion(TimestampModel, table=True):
    ...

class Card(TimestampModel, table=True):
    ...

class Printing(TimestampModel, table=True):
    ...

