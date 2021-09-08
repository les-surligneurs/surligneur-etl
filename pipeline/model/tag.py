from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from model import base


class tag(base):
    __tablename__ = 'tag'

    nomtag = Column(String, primary_key=True)
    article = relationship("commentaire")

    def __int__(self, nomtag: str):
        self.nomtag = nomtag
