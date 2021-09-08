from sqlalchemy import Column, String, Integer, Date
from model import base


class auteurcommentaire(base):
    __tablename__ = 'auteurcommentaire'

    nom = Column(String, primary_key=True)
    profession = Column(String)

    def __init__(self, nom: str, profession: str):
        self.nom = nom
        self.profession = profession
