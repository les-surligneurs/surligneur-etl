from sqlalchemy import Column, String, ForeignKey
from model.tag import tag
from model.source import Source
from model import base

class Commentaire(base):
    __tablename__ = 'commentaire'

    titre = Column(String, primary_key=True)
    corps = Column(String)
    tag = Column(String, ForeignKey(tag.nomtag))
    source = Column(String, ForeignKey(Source.url))
    
    def __init__(self, title: str, corps: str, tag:str, source:str):
        self.title = title
        self.corps = corps
        self.tag = tag
        self.source = source
