from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from model import base


class Source(base):
    __tablename__ = 'source'

    url = Column(String, primary_key=True)
    nature = Column(String)
    auteurs = relationship("auteursource", back_populates="auteursource")

    def __init__(self, url: str, nature: str):
        self.url = url
        self.nature = nature
