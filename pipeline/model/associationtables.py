from model.models import *
from model.models import base

class ecritsource(base):
    __tablename__ = 'ecritsource'

    nomauteursource = Column('nomauteursource',ForeignKey(auteursource.nom), primary_key=True)
    urlsource = Column('urlsource',ForeignKey(Source.url), primary_key=True)
    ecritle = Column('ecritle',DATE)
    source = relationship(Source, back_populates="srcs")
    auteurs = relationship(auteursource, back_populates="auteursource")

class ecritcommentaire(base):
    __tablename__ = 'ecritcommentaire'

    nomauteurcommentaire = Column('nomauteurcommentaire',ForeignKey(auteurcommentaire.nom), primary_key=True)
    titrecommentaire = Column('titrecommentaire',ForeignKey(Commentaire.titre), primary_key=True)
    commenatairedate = Column('datecomm',DATE)
    comment = relationship(Commentaire, back_populates="commentairea")
    auteurscom = relationship(auteurcommentaire, back_populates="auteurcommentaire")


class refloicomm(base):
    __tablename__ = 'refloicomm'

    titrecomm = Column('titrecomm',ForeignKey(Commentaire.titre), primary_key=True)
    urlloi = Column('urlloi',ForeignKey(lienlois.url), primary_key=True)
    phrase = Column(String)
    comment = relationship(Commentaire, back_populates="commloi")
    loicomm = relationship(lienlois, back_populates="lienloiscomm")
