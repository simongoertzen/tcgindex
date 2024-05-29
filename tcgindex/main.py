from .models import LocalizedSetName, LocalizedSetNameCreate, LocalizedSetNameUpdate, LocalizedSetNamePublic, ProtoCard, ProtoCardCreate, ProtoCardUpdate, ProtoCardPublic, CardRepresentation, CardRepresentationCreate, CardRepresentationUpdate, CardRepresentationPublic, LocalizedCardName, LocalizedCardNameCreate, LocalizedCardNameUpdate, LocalizedCardNamePublic

@app.post("/localizedcardname", response_model=LocalizedCardNamePublic)
def create_localizedcardname(*, session: Session = Depends(get_session), localizedcardname: LocalizedCardNameCreate):
    db_localizedcardname = LocalizedCardName.from_orm(localizedcardname)
    session.add(db_localizedcardname)
    session.commit()
    session.refresh(db_localizedcardname)
    return db_localizedcardname

@app.get("/localizedcardname", response_model=list[LocalizedCardNamePublic])
def read_localizedcardnames(*, session: Session = Depends(get_session)):
    localizedcardnames = session.exec(select(LocalizedCardName)).all()
    return localizedcardnames

@app.get("/localizedcardname/{localizedcardname_id}", response_model=LocalizedCardNamePublic)
def read_localizedcardname(*, session: Session = Depends(get_session), localizedcardname_id: int):
    localizedcardname = session.get(LocalizedCardName, localizedcardname_id)
    if not localizedcardname:
        raise HTTPException(status_code=404, detail="LocalizedCardName not found")
    return localizedcardname

@app.put("/localizedcardname/{localizedcardname_id}", response_model=LocalizedCardNamePublic)
def update_localizedcardname(*, session: Session = Depends(get_session), localizedcardname_id: int, localizedcardname: LocalizedCardNameUpdate):
    db_localizedcardname = session.get(LocalizedCardName, localizedcardname_id)
    if not db_localizedcardname:
        raise HTTPException(status_code=404, detail="LocalizedCardName not found")
    localizedcardname_data = localizedcardname.dict(exclude_unset=True)
    for key, value in localizedcardname_data.items():
        setattr(db_localizedcardname, key, value)
    session.add(db_localizedcardname)
    session.commit()
    session.refresh(db_localizedcardname)
    return db_localizedcardname

@app.delete("/localizedcardname/{localizedcardname_id}", response_model=LocalizedCardNamePublic)
def delete_localizedcardname(*, session: Session = Depends(get_session), localizedcardname_id: int):
    localizedcardname = session.get(LocalizedCardName, localizedcardname_id)
    if not localizedcardname:
        raise HTTPException(status_code=404, detail="LocalizedCardName not found")
    session.delete(localizedcardname)
    session.commit()
    return localizedcardname

@app.post("/cardrepresentation", response_model=CardRepresentationPublic)
def create_cardrepresentation(*, session: Session = Depends(get_session), cardrepresentation: CardRepresentationCreate):
    db_cardrepresentation = CardRepresentation.from_orm(cardrepresentation)
    session.add(db_cardrepresentation)
    session.commit()
    session.refresh(db_cardrepresentation)
    return db_cardrepresentation

@app.get("/cardrepresentation", response_model=list[CardRepresentationPublic])
def read_cardrepresentations(*, session: Session = Depends(get_session)):
    cardrepresentations = session.exec(select(CardRepresentation)).all()
    return cardrepresentations

@app.get("/cardrepresentation/{cardrepresentation_id}", response_model=CardRepresentationPublic)
def read_cardrepresentation(*, session: Session = Depends(get_session), cardrepresentation_id: int):
    cardrepresentation = session.get(CardRepresentation, cardrepresentation_id)
    if not cardrepresentation:
        raise HTTPException(status_code=404, detail="CardRepresentation not found")
    return cardrepresentation

@app.put("/cardrepresentation/{cardrepresentation_id}", response_model=CardRepresentationPublic)
def update_cardrepresentation(*, session: Session = Depends(get_session), cardrepresentation_id: int, cardrepresentation: CardRepresentationUpdate):
    db_cardrepresentation = session.get(CardRepresentation, cardrepresentation_id)
    if not db_cardrepresentation:
        raise HTTPException(status_code=404, detail="CardRepresentation not found")
    cardrepresentation_data = cardrepresentation.dict(exclude_unset=True)
    for key, value in cardrepresentation_data.items():
        setattr(db_cardrepresentation, key, value)
    session.add(db_cardrepresentation)
    session.commit()
    session.refresh(db_cardrepresentation)
    return db_cardrepresentation

@app.delete("/cardrepresentation/{cardrepresentation_id}", response_model=CardRepresentationPublic)
def delete_cardrepresentation(*, session: Session = Depends(get_session), cardrepresentation_id: int):
    cardrepresentation = session.get(CardRepresentation, cardrepresentation_id)
    if not cardrepresentation:
        raise HTTPException(status_code=404, detail="CardRepresentation not found")
    session.delete(cardrepresentation)
    session.commit()
    return cardrepresentation

