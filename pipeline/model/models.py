from sqlalchemy import Column, String, ForeignKey, DATE
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

"""
    # Class de la table 'auteursource' et des ses informations
"""
class auteursource(base):
    __tablename__ = 'auteursource'

    nom = Column(String, primary_key=True)
    typesource = Column(String)
    auteursource = relationship("ecritsource", back_populates="auteurs")

    def __init__(self, nom: str, typesource: str):
        self.nom = nom
        self.typesource = typesource

"""
    # Class de la table 'source' et des ses informations
"""
class Source(base):
    __tablename__ = 'sources'

    url = Column(String, primary_key=True)
    nature = Column(String)

    srcs = relationship("ecritsource", back_populates="source")

    def __init__(self, url: str = '', nature: str = ''):
        self.url = url
        self.nature = nature

"""
    # Class de la table 'commentaire' et des ses informations
"""
class Commentaire(base):
    __tablename__ = 'commentaire'

    titre = Column(String, primary_key=True)
    corps = Column(String)
    resume = Column(String)
    tag = Column(String)

    commentairea = relationship("ecritcommentaire", back_populates="comment")
    commloi = relationship("refloicomm", back_populates="comment")

    source_url = Column(String, ForeignKey('sources.url'), unique=True)
    source = relationship("Source", backref=backref("commentaire", uselist=False))

    def __init__(self, title: str, corps: str, resume: str, tag: str):
        self.titre = title
        self.corps = corps
        self.tag = tag
        self.resume = resume

"""
    # Class de la table 'auteurcommentaire' et des ses informations
"""
class auteurcommentaire(base):
    __tablename__ = 'auteurcommentaire'

    nom = Column(String, primary_key=True)
    profession = Column(String)

    auteurcommentaire = relationship("ecritcommentaire", back_populates="auteurscom")

    def __init__(self, nom: str, profession: str):
        self.nom = nom
        self.profession = profession

"""
    # Class de la table 'lienlois' et des ses informations
"""
class lienlois(base):
    __tablename__ = 'lienlois'

    url = Column(String, primary_key=True)
    lienloiscomm = relationship("refloicomm", back_populates="loicomm")

    def __init__(self, url: str):
        self.url = url

"""
    # Class de la table 'resNLP' et des ses informations
"""
class resNLP(base):
    __tablename__ = 'resNLP'

    titrecomm = Column(String, primary_key=True)
    personalite = Column(String)
    lieu = Column(String)

    titre_str = Column(String, ForeignKey('commentaire.titre'), unique=True)
    titre = relationship("Commentaire", backref=backref("commentaire", uselist=False))

    def __init__(self, titre: str, personlite: str = '', lieu: str = ''):
        self.titrecomm = titre
        self.personalite = personlite
        self.lieu = lieu
