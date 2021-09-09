import argparse
import logging
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import base
from model.models import auteursource, auteurcommentaire, resNLP, Commentaire, Source, lienlois
from model.associationtables import ecritsource, ecritcommentaire, refloicomm
from Extracter import Extracter

logging.basicConfig(filename='etl.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


def get_date(string: str):
    dictmois = {
        "janvier": "-01-",
        "février": "-02-",
        "mars": "-03-",
        "avril": "-04-",
        "mai": "-05-",
        "juin": "-06-",
        "juillet": "-07-",
        "août": "-08-",
        "septembre": "-09-",
        "octobre": "-10-",
        "novembre": "-11-",
        "décembre": "-12-"
    }

    data = string.split(" ")
    if (len(data) == 3):
        data.reverse()

        for k, v in dictmois.items():
            data[1] = str(data[1]).replace(k, v)
        date = ""
        for valeur in data:
            date += str(valeur)
        date += ", 00:00:00"
        date = datetime.datetime.strptime(date, '%Y-%m-%d, %H:%M:%S').date()
    else:
        datenow = datetime.datetime.today().strftime('%Y-%m-%d, %H:%M:%S')
        date = datetime.datetime.strptime(datenow,'%Y-%m-%d, %H:%M:%S').date()
    return date


class Config:
    def __init__(self, host: str, port: str, db: str, user: str, pwd: str):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.pwd = pwd

    def __str__(self) -> str:
        return "Host: " + str(self.host) + " -Port: " + str(self.port) + " -Database: " + str(
            self.db) + " -User: " + str(self.user) + " -Password: " + str(self.pwd)


class PGEngine:
    def __init__(self, config: Config):
        self.configuration = config
        # 'postgresql://usr:pass@localhost:5432/sqlalchemy'
        self.cnxString = "postgresql://" + str(self.configuration.user) + ":" + str(self.configuration.pwd) + "@" + str(
            self.configuration.host) + ":" + str(self.configuration.port) + "/" + str(self.configuration.db)
        logging.info("%s", self.cnxString)
        self.engine = create_engine(self.cnxString)
        self.session = sessionmaker(bind=self.engine)
        self.Session = self.session()
        base.metadata.create_all(self.engine)

    def insertTuple(self, obj: any):
        logging.info("Insertion du tuple")
        self.Session.merge(obj)
        self.Session.commit()

    def closeSession(self):
        self.Session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Pipeline d\'intégration de données du site les surligneurs')
    parser.add_argument("--host", dest="host",
                        help="Adresse de la base de donnée cible")
    parser.add_argument("--port", dest="port", help="Port de la machine cible")
    parser.add_argument("--db", dest="db", help="Base de donnée cible")
    parser.add_argument("--user", dest="user", help="Pseudonyme utilisateur")
    parser.add_argument("--pwd", dest="pwd", help="Mot de passe utilisateur")

    args = parser.parse_args()
    logging.info("%s", args)

    conf = Config(args.host, args.port, args.db, args.user, args.pwd)
    logging.info("%s", conf)

    connexion = PGEngine(conf)
    extr = Extracter()

    donnees = extr.get_articles()
    logging.info(len(donnees))
    try:
        for elt in donnees:
            comm = Commentaire(elt[1], elt[11], elt[10], elt[6])
            for x, y in list(zip(elt[3], elt[4])):
                author = auteursource(x, y)
                connexion.insertTuple(author)
            src = Source(elt[0], 'nd')
            for x, y in list(zip(elt[7], elt[8])):
                auteurcom = auteurcommentaire(x, y)
                connexion.insertTuple(auteurcom)
            for lois in elt[13][0::2]:
                connexion.insertTuple(lienlois(lois))
            connexion.insertTuple(comm)
            connexion.insertTuple(src)
            connexion.insertTuple(ecritsource(author.nom,src.url,get_date(elt[5])))
            connexion.insertTuple(ecritcommentaire(auteurcom.nom,comm.titre,get_date(elt[9])))
            if len(elt[13]) > 0:
                i = 0
                while i < len(elt[13]):
                    if i % 2 == 0:
                        url = elt[13][i]
                        phrase = elt[13][i+1]
                        connexion.insertTuple(refloicomm(elt[1],url,phrase))
                    i = i+2
    finally:
        logging.info("Fin de l'importation des données")

    connexion.closeSession()



