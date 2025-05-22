import datetime
from typing import Any

from sqlalchemy import DateTime, func, text
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class PublicModel(SQLModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


# CATALOG
class CatalogBase(SQLModel):
    name: str = Field(unique=True)


class Catalog(CatalogBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    set_representations: list["SetRepresentation"] = Relationship(
        back_populates="catalog"
    )


class CatalogPublic(CatalogBase, PublicModel):
    pass


class CatalogCreate(CatalogBase):
    pass


class CatalogUpdate(CatalogBase):
    name: str | None = None


# GAME
class GameBase(SQLModel):
    name: str


class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    proto_sets: list["ProtoSet"] = Relationship(back_populates="game")
    proto_cards: list["ProtoCard"] = Relationship(back_populates="game")


class GamePublic(PublicModel, GameBase):
    pass


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    name: str | None = None


# PROTO SET
class ProtoSetBase(SQLModel):
    game_id: int = Field(foreign_key="game.id")
    name: str


class ProtoSet(ProtoSetBase, table=True):
    __tablename__ = "proto_set"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    game: Game = Relationship(back_populates="proto_sets")
    set_representations: list["SetRepresentation"] = Relationship(
        back_populates="proto_set"
    )


class ProtoSetCreate(ProtoSetBase):
    pass


class ProtoSetPublic(ProtoSetBase, PublicModel):
    pass


class ProtoSetUpdate(ProtoSetBase):
    game_id: int | None = None
    name: str | None = None


# SET REPRESENTATION
class SetRepresentationBase(SQLModel):
    proto_set_id: int = Field(foreign_key="proto_set.id")
    catalog_id: int = Field(foreign_key="catalog.id")
    name: str
    identifier: str
    size: int
    # catalog_data: dict[str, Any] = Field(sa_column=Column(JSON))


class SetRepresentation(SetRepresentationBase, table=True):
    __tablename__ = "set_representation"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    proto_set: ProtoSet = Relationship(back_populates="set_representations")
    catalog: Catalog = Relationship(back_populates="set_representations")
    localized_names: list["LocalizedSetName"] = Relationship(
        back_populates="set_representation"
    )
    card_representations: list["CardRepresentation"] = Relationship(
        back_populates="set_representation"
    )


class SetRepresentationCreate(SetRepresentationBase):
    pass


class SetRepresentationPublic(SetRepresentationBase, PublicModel):
    pass


class SetRepresentationUpdate(SetRepresentationBase):
    proto_set_id: int | None = None
    catalog_id: int | None = None
    name: str | None = None
    identifier: str | None = None
    size: int | None = None
    # catalog_data: dict[str, Any] | None = None


# LOCALIZED SET NAME
class LocalizedSetNameBase(SQLModel):
    set_representation_id: int = Field(foreign_key="set_representation.id")
    name: str
    locale: str


class LocalizedSetName(LocalizedSetNameBase, table=True):
    __tablename__ = "localized_set_name"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    set_representation: SetRepresentation = Relationship(
        back_populates="localized_names"
    )


class LocalizedSetNameCreate(LocalizedSetNameBase):
    pass


class LocalizedSetNamePublic(LocalizedSetNameBase, PublicModel):
    pass


class LocalizedSetNameUpdate(LocalizedSetNameBase):
    set_representation_id: int | None = None
    name: str | None = None
    locale: str | None = None


# PROTO CARD
class ProtoCardBase(SQLModel):
    """
    A prototype card must not point to a prototype set, as the prototype set(s) of a card
    are determined by the set representations in the respective catalogs:
    CardRepresentation -> SetRepresentation -> ProtoSet and
    CardRepresentation -> ProtoCard -/-> ProtoSet to ensure data integitry
    """

    game_id: int = Field(foreign_key="game.id")
    name: str


class ProtoCard(ProtoCardBase, table=True):
    __tablename__ = "proto_card"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    game: Game = Relationship(back_populates="proto_cards")
    card_representations: list["CardRepresentation"] = Relationship(
        back_populates="proto_card"
    )


class ProtoCardCreate(ProtoCardBase):
    pass


class ProtoCardPublic(ProtoCardBase, PublicModel):
    pass


class ProtoCardUpdate(ProtoCardBase):
    game_id: int | None = None
    name: str | None = None


# CARD REPRESENTATION
class CardRepresentationBase(SQLModel):
    game_id: int = Field(foreign_key="game.id")
    proto_card_id: int = Field(foreign_key="proto_card.id")
    set_representation_id: int = Field(foreign_key="set_representation.id")
    name: str
    identifier: str
    # catalog_data: dict[str, Any] = Field(sa_column=Column(JSON))


class CardRepresentation(CardRepresentationBase, table=True):
    __tablename__ = "card_representation"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    game: Game = Relationship(back_populates="game")
    prototype: ProtoCard = Relationship(back_populates="representations")
    set_representation: SetRepresentation = Relationship(
        back_populates="card_representations"
    )
    localized_names: list["LocalizedCardName"] = Relationship(
        back_populates="card_representation"
    )


class CardRepresentationCreate(CardRepresentationBase):
    pass


class CardRepresentationPublic(CardRepresentationBase, PublicModel):
    pass


class CardRepresentationUpdate(CardRepresentationBase):
    game_id: int | None = None
    proto_card_id: int | None = None
    set_representation_id: int | None = None
    name: str | None = None
    identifier: str | None = None
    # catalog_data: dict[str, Any] | None = None


# LOCALIZED CARD NAME
class LocalizedCardNameBase(SQLModel):
    card_representation_id: int = Field(foreign_key="card_representation.id")
    name: str
    locale: str


class LocalizedCardName(LocalizedCardNameBase, table=True):
    __tablename__ = "localized_card_name"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    updated_at: datetime.datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    card_representation: CardRepresentation = Relationship(
        back_populates="localized_names"
    )


class LocalizedCardNameCreate(LocalizedCardNameBase):
    pass


class LocalizedCardNamePublic(LocalizedCardNameBase, PublicModel):
    pass


class LocalizedCardNameUpdate(LocalizedCardNameBase):
    card_representation_id: int | None = None
    name: str | None = None
    locale: str | None = None
