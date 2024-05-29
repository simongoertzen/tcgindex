import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import DateTime, func, text
from sqlmodel import Column, Field, SQLModel, Relationship
class GameBase(SQLModel):
    name: str


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
    name: str = Field(unique=True)
    set_representations: list["SetRepresentation"] = Relationship(
        back_populates="catalog"
    )


class Game(TimestampModel, GameBase, table=True):
    proto_sets: list["ProtoSet"] = Relationship(back_populates="game")
    proto_cards: list["ProtoCard"] = Relationship(back_populates="game")
class ProtoSet(TimestampModel, table=True):
    game_id: int = Field(foreign_key="game.id")
    game: Game = Relationship(back_populates="proto_sets")
    set_representations: list["SetRepresentation"] = Relationship(
        back_populates="proto_set"
    )


class SetRepresentation(TimestampModel, table=True):
    proto_set_id: int = Field(foreign_key="proto_set.id")
    proto_set: ProtoSet = Relationship(back_populates="set_representations")
    catalog_id: int = Field(foreign_key="catalog.id")
    catalog: Catalog = Relationship(back_populates="set_representations")
    name: str
    localized_names: list["LocalizedSetName"] = Relationship(
        back_populates="set_representation"
    )
    str_code: str
    int_code: int | None
    uuid_code: UUID | None
    catalog_data: dict[str, Any]
    card_representations: list["CardRepresentation"] = Relationship(
        back_populates="set_representation"
    )


class LocalizedSetName(TimestampModel, table=True):
    set_representation_id: int = Field(foreign_key="set_representation.id")
    set_representation: SetRepresentation = Relationship(
        back_populates="localized_names"
    )
    name: str
    locale: str


class ProtoCard(TimestampModel, table=True):
    """
    A prototype card must not point to a prototype set, as the prototype set(s) of a card
    are determined by the set representations in the respective catalogs:
    CardRepresentation -> SetRepresentation -> ProtoSet and
    CardRepresentation -> ProtoCard -/-> ProtoSet to ensure data integitry
    """

    game_id: int = Field(foreign_key="game.id")
    game: Game = Relationship(back_populates="proto_cards")
    card_representations: list["CardRepresentation"] = Relationship(
        back_populates="proto_card"
    )


class CardRepresentation(TimestampModel, table=True):
    game_id: int = Field(foreign_key="game.id")
    game: Game = Relationship(back_populates="game")
    proto_card_id: int = Field(foreign_key="proto_card.id")
    prototype: ProtoCard = Relationship(back_populates="representations")
    set_representation_id: int = Field(foreign_key="set_representation.id")
    set_representation: SetRepresentation = Relationship(
        back_populates="card_representations"
    )
    name: str
    localized_names: list["LocalizedCardName"] = Relationship(
        back_populates="card_representation"
    )
    str_code: str
    int_code: int | None
    uuid_code: UUID | None
    catalog_data: dict[str, Any]


class LocalizedCardName(TimestampModel, table=True):
    card_representation_id: int = Field(foreign_key="card_representation.id")
    card_representation: CardRepresentation = Relationship(
        back_populates="localized_names"
    )
    name: str
    locale: str


class GameCreate(SQLModel):
    name: str

class GamePublic(SQLModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class GameUpdate(SQLModel):
    name: str | None = None






