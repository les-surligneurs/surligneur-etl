from sqlalchemy import Table, Column, Integer, ForeignKey, DATE, String
from model.commentaire import Commentaire
from model import base

class resNLP(base):
    __tablename__ = 'resNLP'

    titrecomm = Column(String,primary_key=True)
    personalite = Column(String)
    lieu = Column(String)

    def __init__(self, titre: str, personlite: str ='', lieu: str = ''):
        self.titrecomm = titre
        self.personalite = personlite
        self.lieu = lieu