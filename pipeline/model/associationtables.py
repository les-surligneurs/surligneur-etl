import datetime

from model.models import *
from model.models import base

class ecritsource(base):
    __tablename__ = 'ecritsource'

    nomauteursource = Column('nomauteursource',ForeignKey(auteursource.nom), primary_key=True)
    urlsource = Column('urlsource',ForeignKey(Source.url), primary_key=True)
    ecritle = Column('ecritle',DATE)
    source = relationship(Source, back_populates="srcs")
    auteurs = relationship(auteursource, back_populates="auteursource")

    def __init__(self, auteur:str,url: str,date: datetime.date):
        self.urlsource = url
        self.nomauteursource = auteur
        self.ecritle = date


class ecritcommentaire(base):
    __tablename__ = 'ecritcommentaire'

    nomauteurcommentaire = Column('nomauteurcommentaire',ForeignKey(auteurcommentaire.nom), primary_key=True)
    titrecommentaire = Column('titrecommentaire',ForeignKey(Commentaire.titre), primary_key=True)
    commenatairedate = Column('datecomm',DATE)
    comment = relationship(Commentaire, back_populates="commentairea")
    auteurscom = relationship(auteurcommentaire, back_populates="auteurcommentaire")

    def __init__(self, auteur:str, titre:str, date:datetime.date):
        self.nomauteurcommentaire = auteur
        self.titrecommentaire = titre
        self.commenatairedate = date

class refloicomm(base):
    __tablename__ = 'refloicomm'

    titrecomm = Column('titrecomm',ForeignKey(Commentaire.titre), primary_key=True)
    urlloi = Column('urlloi',ForeignKey(lienlois.url), primary_key=True)
    phrase = Column(String)
    comment = relationship(Commentaire, back_populates="commloi")
    loicomm = relationship(lienlois, back_populates="lienloiscomm")

    def __init__(self, titre:str, url:str, phrase:str):
        self.titrecomm = titre
        self.urlloi = url
        self.phrase = phrase