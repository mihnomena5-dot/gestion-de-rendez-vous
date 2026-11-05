from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#adress base de données
DATABASE_URL = "sqlite:///./rendezvous.db"

#connexion base de données
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#creation des sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
