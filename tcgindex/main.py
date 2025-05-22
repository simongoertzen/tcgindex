from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from tcgindex.models import (
    PublicModel,
    Catalog,
    CatalogPublic,
    CatalogCreate,
    CatalogUpdate,
    Game,
    GamePublic,
    GameCreate,
    GameUpdate,
    ProtoSet,
    ProtoSetPublic,
    ProtoSetCreate,
    ProtoSetUpdate,
    SetRepresentation,
    SetRepresentationPublic,
    SetRepresentationCreate,
    SetRepresentationUpdate,
    LocalizedSetName,
    LocalizedSetNamePublic,
    LocalizedSetNameCreate,
    LocalizedSetNameUpdate,
    ProtoCard,
    ProtoCardPublic,
    ProtoCardCreate,
    ProtoCardUpdate,
    CardRepresentation,
    CardRepresentationPublic,
    CardRepresentationCreate,
    CardRepresentationUpdate,
    LocalizedCardName,
    LocalizedCardNamePublic,
    LocalizedCardNameCreate,
    LocalizedCardNameUpdate,
)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def get_engine():
    return engine


def create_db_and_tables():
    Path(sqlite_file_name).unlink(missing_ok=True)
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def crud_factory(
    name: str,
    db_model: type[SQLModel],
    public_model: type[PublicModel],
    create_model: type[SQLModel],
    update_model: type[SQLModel],
):
    endpoint = f"/{name}"
    endpoint_with_id = endpoint + "/{id}"

    def get(session, id):
        db_instance = session.get(db_model, id)
        if not db_instance:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return db_instance

    def create(instance: create_model):
        with Session(engine) as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance

    def read_many():
        with Session(engine) as session:
            result = list(session.exec(select(db_model)).all())
            return result

    def read_one(id: int):
        with Session(engine) as session:
            return get(session, id)

    def update(id: int, patch: update_model):
        with Session(engine) as session:
            db_instance = get(session, id)
            patch_data = patch.model_dump(exclude_unset=True)
            db_instance.sqlmodel_update(patch_data)
            session.add(db_instance)
            session.commit()
            session.refresh(db_instance)
            return db_instance

    def delete(id: int):
        with Session(engine) as session:
            db_instance = get(session, id)
            session.delete(db_instance)
            session.commit()
            return db_instance

    app.post(endpoint, response_model=public_model, name=f"{name} create")(create)
    app.get(endpoint, response_model=list[public_model], name=f"{name} read many")(
        read_many
    )
    app.get(endpoint_with_id, response_model=public_model, name=f"{name} read one")(
        read_one
    )
    app.patch(endpoint_with_id, response_model=public_model, name=f"{name} update")(
        update
    )
    app.delete(endpoint_with_id, response_model=public_model, name=f"{name} delete")(
        delete
    )


for setup in [
    ["catalog", Catalog, CatalogPublic, CatalogCreate, CatalogUpdate],
    ["game", Game, GamePublic, GameCreate, GameUpdate],
    ["proto_set", ProtoSet, ProtoSetPublic, ProtoSetCreate, ProtoSetUpdate],
    [
        "set_representation",
        SetRepresentation,
        SetRepresentationPublic,
        SetRepresentationCreate,
        SetRepresentationUpdate,
    ],
    [
        "localized_set_name",
        LocalizedSetName,
        LocalizedSetNamePublic,
        LocalizedSetNameCreate,
        LocalizedSetNameUpdate,
    ],
    ["proto_card", ProtoCard, ProtoCardPublic, ProtoCardCreate, ProtoCardUpdate],
    [
        "card_representation",
        CardRepresentation,
        CardRepresentationPublic,
        CardRepresentationCreate,
        CardRepresentationUpdate,
    ],
    [
        "localized_card_name",
        LocalizedCardName,
        LocalizedCardNamePublic,
        LocalizedCardNameCreate,
        LocalizedCardNameUpdate,
    ],
]:
    crud_factory(*setup)


if __name__ == "__main__":
    create_db_and_tables()


if False:

    @app.post("/catalog", response_model=CatalogPublic)
    def create_catalog(catalog: CatalogCreate):
        with Session(engine) as session:
            session.add(catalog)
            session.commit()
            session.refresh(catalog)
            return catalog

    @app.get("/catalog", response_model=list[CatalogPublic])
    def read_catalogs():
        with Session(engine) as session:
            catalogs = session.exec(select(Catalog)).all()
            return catalogs

    @app.get("/catalog/{catalog_id}", response_model=CatalogPublic)
    def read_catalog(catalog_id: int):
        with Session(engine) as session:
            catalog = session.get(Catalog, catalog_id)
            if not catalog:
                raise HTTPException(status_code=404, detail="Catalog not found")
            return catalog

    @app.patch("/catalog/{catalog_id}", response_model=CatalogPublic)
    def update_catalog(catalog_id: int, catalog: CatalogUpdate):
        with Session(engine) as session:
            db_catalog = session.get(Catalog, catalog_id)
            if not db_catalog:
                raise HTTPException(status_code=404, detail="Catalog not found")
            patch_data = catalog.model_dump(exclude_unset=True)
            db_catalog.sqlmodel_update(patch_data)
            session.add(db_catalog)
            session.commit()
            session.refresh(db_catalog)
            return db_catalog

    @app.delete("/catalog/{catalog_id}", response_model=CatalogPublic)
    def delete_catalog(catalog_id: int):
        with Session(engine) as session:
            catalog = session.get(Catalog, catalog_id)
            if not catalog:
                raise HTTPException(status_code=404, detail="Catalog not found")
            session.delete(catalog)
            session.commit()
            return catalog

    @app.post("/game", response_model=GamePublic)
    def create_game(game: GameCreate):
        with Session(engine) as session:
            session.add(game)
            session.commit()
            session.refresh(game)
            return game

    @app.get("/game", response_model=list[GamePublic])
    def read_games():
        with Session(engine) as session:
            games = session.exec(select(Game)).all()
            return games

    @app.get("/game/{game_id}", response_model=GamePublic)
    def read_game(game_id: int):
        with Session(engine) as session:
            game = session.get(Game, game_id)
            if not game:
                raise HTTPException(status_code=404, detail="Game not found")
            return game

    @app.patch("/game/{game_id}", response_model=GamePublic)
    def update_game(game_id: int, game: GameUpdate):
        with Session(engine) as session:
            db_game = session.get(Game, game_id)
            if not db_game:
                raise HTTPException(status_code=404, detail="Game not found")
            patch_data = game.model_dump(exclude_unset=True)
            db_game.sqlmodel_update(patch_data)
            session.add(db_game)
            session.commit()
            session.refresh(db_game)
            return db_game

    @app.delete("/game/{game_id}", response_model=GamePublic)
    def delete_game(game_id: int):
        with Session(engine) as session:
            game = session.get(Game, game_id)
            if not game:
                raise HTTPException(status_code=404, detail="Game not found")
            session.delete(game)
            session.commit()
            return game

    @app.post("/proto_set", response_model=ProtoSetPublic)
    def create_proto_set(proto_set: ProtoSetCreate):
        with Session(engine) as session:
            session.add(proto_set)
            session.commit()
            session.refresh(proto_set)
            return proto_set

    @app.get("/proto_set", response_model=list[ProtoSetPublic])
    def read_proto_sets():
        with Session(engine) as session:
            proto_sets = session.exec(select(ProtoSet)).all()
            return proto_sets

    @app.get("/proto_set/{proto_set_id}", response_model=ProtoSetPublic)
    def read_proto_set(proto_set_id: int):
        with Session(engine) as session:
            proto_set = session.get(ProtoSet, proto_set_id)
            if not proto_set:
                raise HTTPException(status_code=404, detail="ProtoSet not found")
            return proto_set

    @app.patch("/proto_set/{proto_set_id}", response_model=ProtoSetPublic)
    def update_proto_set(
        proto_set_id: int,
        proto_set: ProtoSetUpdate,
    ):
        with Session(engine) as session:
            db_proto_set = session.get(ProtoSet, proto_set_id)
            if not db_proto_set:
                raise HTTPException(status_code=404, detail="ProtoSet not found")
            patch_data = proto_set.model_dump(exclude_unset=True)
            db_proto_set.sqlmodel_update(patch_data)
            session.add(db_proto_set)
            session.commit()
            session.refresh(db_proto_set)
            return db_proto_set

    @app.delete("/proto_set/{proto_set_id}", response_model=ProtoSetPublic)
    def delete_proto_set(proto_set_id: int):
        with Session(engine) as session:
            proto_set = session.get(ProtoSet, proto_set_id)
            if not proto_set:
                raise HTTPException(status_code=404, detail="ProtoSet not found")
            session.delete(proto_set)
            session.commit()
            return proto_set

    @app.post("/set_representation", response_model=SetRepresentationPublic)
    def create_set_representation(
        set_representation: SetRepresentationCreate,
    ):
        with Session(engine) as session:
            session.add(set_representation)
            session.commit()
            session.refresh(set_representation)
            return set_representation

    @app.get("/set_representation", response_model=list[SetRepresentationPublic])
    def read_set_representations():
        with Session(engine) as session:
            set_representations = session.exec(select(SetRepresentation)).all()
            return set_representations

    @app.get(
        "/set_representation/{set_representation_id}",
        response_model=SetRepresentationPublic,
    )
    def read_set_representation(set_representation_id: int):
        with Session(engine) as session:
            set_representation = session.get(SetRepresentation, set_representation_id)
            if not set_representation:
                raise HTTPException(
                    status_code=404, detail="SetRepresentation not found"
                )
            return set_representation

    @app.patch(
        "/set_representation/{set_representation_id}",
        response_model=SetRepresentationPublic,
    )
    def update_set_representation(
        set_representation_id: int,
        set_representation: SetRepresentationUpdate,
    ):
        with Session(engine) as session:
            db_set_representation = session.get(
                SetRepresentation, set_representation_id
            )
            if not db_set_representation:
                raise HTTPException(
                    status_code=404, detail="SetRepresentation not found"
                )
            patch_data = set_representation.model_dump(exclude_unset=True)
            db_set_representation.sqlmodel_update(patch_data)
            session.add(db_set_representation)
            session.commit()
            session.refresh(db_set_representation)
            return db_set_representation

    @app.delete(
        "/set_representation/{set_representation_id}",
        response_model=SetRepresentationPublic,
    )
    def delete_set_representation(set_representation_id: int):
        with Session(engine) as session:
            set_representation = session.get(SetRepresentation, set_representation_id)
            if not set_representation:
                raise HTTPException(
                    status_code=404, detail="SetRepresentation not found"
                )
            session.delete(set_representation)
            session.commit()
            return set_representation

    @app.post("/localized_set_name", response_model=LocalizedSetNamePublic)
    def create_localized_set_name(localized_set_name: LocalizedSetNameCreate):
        with Session(engine) as session:
            session.add(localized_set_name)
            session.commit()
            session.refresh(localized_set_name)
            return localized_set_name

    @app.get("/localized_set_name", response_model=list[LocalizedSetNamePublic])
    def read_localized_set_names():
        with Session(engine) as session:
            localized_set_names = session.exec(select(LocalizedSetName)).all()
            return localized_set_names

    @app.get(
        "/localized_set_name/{localized_set_name_id}",
        response_model=LocalizedSetNamePublic,
    )
    def read_localized_set_name(localized_set_name_id: int):
        with Session(engine) as session:
            localized_set_name = session.get(LocalizedSetName, localized_set_name_id)
            if not localized_set_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedSetName not found"
                )
            return localized_set_name

    @app.patch(
        "/localized_set_name/{localized_set_name_id}",
        response_model=LocalizedSetNamePublic,
    )
    def update_localized_set_name(
        localized_set_name_id: int,
        localized_set_name: LocalizedSetNameUpdate,
    ):
        with Session(engine) as session:
            db_localized_set_name = session.get(LocalizedSetName, localized_set_name_id)
            if not db_localized_set_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedSetName not found"
                )
            patch_data = localized_set_name.model_dump(exclude_unset=True)
            db_localized_set_name.sqlmodel_update(patch_data)
            session.add(db_localized_set_name)
            session.commit()
            session.refresh(db_localized_set_name)
            return db_localized_set_name

    @app.delete(
        "/localized_set_name/{localized_set_name_id}",
        response_model=LocalizedSetNamePublic,
    )
    def delete_localized_set_name(localized_set_name_id: int):
        with Session(engine) as session:
            localized_set_name = session.get(LocalizedSetName, localized_set_name_id)
            if not localized_set_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedSetName not found"
                )
            session.delete(localized_set_name)
            session.commit()
            return localized_set_name

    @app.post("/proto_card", response_model=ProtoCardPublic)
    def create_proto_card(proto_card: ProtoCardCreate):
        with Session(engine) as session:
            session.add(proto_card)
            session.commit()
            session.refresh(proto_card)
            return proto_card

    @app.get("/proto_card", response_model=list[ProtoCardPublic])
    def read_proto_cards():
        with Session(engine) as session:
            proto_cards = session.exec(select(ProtoCard)).all()
            return proto_cards

    @app.get("/proto_card/{proto_card_id}", response_model=ProtoCardPublic)
    def read_proto_card(proto_card_id: int):
        with Session(engine) as session:
            proto_card = session.get(ProtoCard, proto_card_id)
            if not proto_card:
                raise HTTPException(status_code=404, detail="ProtoCard not found")
            return proto_card

    @app.patch("/proto_card/{proto_card_id}", response_model=ProtoCardPublic)
    def update_proto_card(
        proto_card_id: int,
        proto_card: ProtoCardUpdate,
    ):
        with Session(engine) as session:
            db_proto_card = session.get(ProtoCard, proto_card_id)
            if not db_proto_card:
                raise HTTPException(status_code=404, detail="ProtoCard not found")
            patch_data = proto_card.model_dump(exclude_unset=True)
            db_proto_card.sqlmodel_update(patch_data)
            session.add(db_proto_card)
            session.commit()
            session.refresh(db_proto_card)
            return db_proto_card

    @app.delete("/proto_card/{proto_card_id}", response_model=ProtoCardPublic)
    def delete_proto_card(proto_card_id: int):
        with Session(engine) as session:
            proto_card = session.get(ProtoCard, proto_card_id)
            if not proto_card:
                raise HTTPException(status_code=404, detail="ProtoCard not found")
            session.delete(proto_card)
            session.commit()
            return proto_card

    @app.post("/card_representation", response_model=CardRepresentationPublic)
    def create_card_representation(
        card_representation: CardRepresentationCreate,
    ):
        with Session(engine) as session:
            session.add(card_representation)
            session.commit()
            session.refresh(card_representation)
            return card_representation

    @app.get("/card_representation", response_model=list[CardRepresentationPublic])
    def read_card_representations():
        with Session(engine) as session:
            card_representations = session.exec(select(CardRepresentation)).all()
            return card_representations

    @app.get(
        "/card_representation/{card_representation_id}",
        response_model=CardRepresentationPublic,
    )
    def read_card_representation(card_representation_id: int):
        with Session(engine) as session:
            card_representation = session.get(
                CardRepresentation, card_representation_id
            )
            if not card_representation:
                raise HTTPException(
                    status_code=404, detail="CardRepresentation not found"
                )
            return card_representation

    @app.patch(
        "/card_representation/{card_representation_id}",
        response_model=CardRepresentationPublic,
    )
    def update_card_representation(
        card_representation_id: int,
        card_representation: CardRepresentationUpdate,
    ):
        with Session(engine) as session:
            db_card_representation = session.get(
                CardRepresentation, card_representation_id
            )
            if not db_card_representation:
                raise HTTPException(
                    status_code=404, detail="CardRepresentation not found"
                )
            patch_data = card_representation.model_dump(exclude_unset=True)
            db_card_representation.sqlmodel_update(patch_data)
            session.add(db_card_representation)
            session.commit()
            session.refresh(db_card_representation)
            return db_card_representation

    @app.delete(
        "/card_representation/{card_representation_id}",
        response_model=CardRepresentationPublic,
    )
    def delete_card_representation(card_representation_id: int):
        with Session(engine) as session:
            card_representation = session.get(
                CardRepresentation, card_representation_id
            )
            if not card_representation:
                raise HTTPException(
                    status_code=404, detail="CardRepresentation not found"
                )
            session.delete(card_representation)
            session.commit()
            return card_representation

    @app.post("/localized_card_name", response_model=LocalizedCardNamePublic)
    def create_localized_card_name(localized_card_name: LocalizedCardNameCreate):
        with Session(engine) as session:
            session.add(localized_card_name)
            session.commit()
            session.refresh(localized_card_name)
            return localized_card_name

    @app.get("/localized_card_name", response_model=list[LocalizedCardNamePublic])
    def read_localized_card_names():
        with Session(engine) as session:
            localized_card_names = session.exec(select(LocalizedCardName)).all()
            return localized_card_names

    @app.get(
        "/localized_card_name/{localized_card_name_id}",
        response_model=LocalizedCardNamePublic,
    )
    def read_localized_card_name(localized_card_name_id: int):
        with Session(engine) as session:
            localized_card_name = session.get(LocalizedCardName, localized_card_name_id)
            if not localized_card_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedCardName not found"
                )
            return localized_card_name

    @app.patch(
        "/localized_card_name/{localized_card_name_id}",
        response_model=LocalizedCardNamePublic,
    )
    def update_localized_card_name(
        localized_card_name_id: int,
        localized_card_name: LocalizedCardNameUpdate,
    ):
        with Session(engine) as session:
            db_localized_card_name = session.get(
                LocalizedCardName, localized_card_name_id
            )
            if not db_localized_card_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedCardName not found"
                )
            patch_data = localized_card_name.model_dump(exclude_unset=True)
            db_localized_card_name.sqlmodel_update(patch_data)
            session.add(db_localized_card_name)
            session.commit()
            session.refresh(db_localized_card_name)
            return db_localized_card_name

    @app.delete(
        "/localized_card_name/{localized_card_name_id}",
        response_model=LocalizedCardNamePublic,
    )
    def delete_localized_card_name(localized_card_name_id: int):
        with Session(engine) as session:
            localized_card_name = session.get(LocalizedCardName, localized_card_name_id)
            if not localized_card_name:
                raise HTTPException(
                    status_code=404, detail="LocalizedCardName not found"
                )
            session.delete(localized_card_name)
            session.commit()
            return localized_card_name
