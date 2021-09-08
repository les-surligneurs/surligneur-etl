import argparse
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import base
from model.tag import tag
from model.source import Source
from model.auteursource import auteursource
from model.auteurcommentaire import auteurcommentaire
from model.commentaire import Commentaire
from model.associationtables import ecritsource, ecritcommentaire,lienlois,refloicomm
from model.lienlois import lienlois
from model.resNLP import resNLP

# TODO: Déplacer le fichier de logs
logging.basicConfig(filename='etl.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


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
        # TODO: Ajouter des logs INFO et ERROR
        logging.info("Insertion du tuple")
        self.Session.add(obj)
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

    connexion.closeSession()
