from sqlalchemy import Table, Column, Integer, ForeignKey, DATE, String
from sqlalchemy.orm import relationship
from model.auteursource import auteursource
from model.source import Source
from model.auteurcommentaire import auteurcommentaire
from model.commentaire import Commentaire
from model.lienlois import lienlois
from model import base

class ecritsource(base):
    __tablename__ = 'ecritsource'

    nomauteursource = Column('nomauteursource',ForeignKey(auteursource.nom), primary_key=True)
    urlsource = Column('urlsource',ForeignKey(Source.url), primary_key=True)
    ecritle = Column('ecritle',DATE)
    source = relationship("source", back_populates="source")
    auteurs = relationship("auteursource", back_populates="auteursource")

class ecritcommentaire(base):
    __tablename__ = 'ecritcommentaire'

    nomauteurcommentaire = Column('nomauteurcommentaire',ForeignKey(auteursource.nom), primary_key=True)
    titrecommentaire = Column('titrecommentaire',ForeignKey(Commentaire.titre), primary_key=True)
    commenatairedate = Column('datecomm',DATE)
    comment = relationship("commentaire", back_populates="commenaitre")
    auteurscom = relationship("auteurcommentaire", back_populates="auteurcommentaire")


class refloicomm(base):
    __tablename__ = 'refloicomm'

    titrecomm = Column('titrecomm',ForeignKey(Commentaire.titre), primary_key=True)
    urlloi = Column('urlloi',ForeignKey(lienlois.url), primary_key=True)
    phrase = Column(String)
    comment = relationship("commentaire", back_populates="commenaitre")
    loi = relationship("lienlois", back_populates="lienlois")
