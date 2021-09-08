from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from model import base


class auteursource(base):
    __tablename__ = 'auteursource'

    nom = Column(String, primary_key=True)
    typesource = Column(String)
    source = relationship("source", back_populates="sources")

    def __init__(self, nom: str, typesource: str):
        self.nom = nom
        self.typesource = typesource
