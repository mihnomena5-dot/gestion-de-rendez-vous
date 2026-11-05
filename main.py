from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

from database import Base, engine, SessionLocal

app = FastAPI()

#table rendez-vous
class RendezVous (Base):
    __tablename__ = "rendezvous"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    date = Column(String)
    heure = Column(String)
    motif = Column(String)

Base.metadata.create_all(bind=engine)

#connexion à la base de donnée
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# info d'un rendez-vous
class RendezVousCreate(BaseModel):
    nom: str
    date: str
    heure: str
    motif: str

#acceuil
@app.get("/")
def acceuil():
    return {"message": "Gestion des rendez-vous"}

#ajouter un rendez-vous
@app.post("/rendezvous/")
def ajouter_rendezvous(
    rdv: RendezVousCreate, 
    db: Session = Depends(get_db)
):
    nouveau = RendezVous(
        nom=rdv.nom,
        date=rdv.date,
        heure=rdv.heure,
        motif=rdv.motif
    )

    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)

    return nouveau

#afficher le rendez-vous
@app.get("/rendezvous/")
def afficher_rendezvous(db: Session = Depends(get_db)):
    return db.query(RendezVous).all()

#supprimer un rendez-vous
@app.delete("/rendezvous/{id}")
def supprimer_rendezvous(
    id: int,
    db: Session = Depends(get_db)
):
    rdv = db.query(RendezVous).filter(
        RendezVous.id == id
    ).first()

    if rdv is None:
        raise HTTPException(
            status_code=404,
            detail="Rendez-vous introuvable"
        ) 

    db.delete(rdv)
    db.commit()

    return {"message": "Rendez-vous supprimé"}
