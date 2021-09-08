DROP DATABASE IF EXISTS lessurligneurs;
CREATE DATABASE lessurligneurs;

DROP TABLE IF EXISTS lienlois;
CREATE TABLE lienlois(
	url TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS auteursource CASCADE;
CREATE TABLE auteursource(
	nom VARCHAR(100) PRIMARY KEY,
	typesource VARCHAR(100)
);

DROP TABLE IF EXISTS auteurcommentaire CASCADE;
CREATE TABLE auteurcommentaire(
	nom  VARCHAR(150),
	profession VARCHAR(50),
	PRIMARY KEY (nom)
);

DROP TABLE IF EXISTS source CASCADE;
CREATE TABLE source(
	url TEXT PRIMARY KEY,
	nature VARCHAR(20)
);

DROP TABLE IF EXISTS commentaire CASCADE;
CREATE TABLE commentaire(
	titre VARCHAR(350) PRIMARY KEY,
	corps TEXT NOT NULL,
	tag VARCHAR(50), 
	source TEXT NOT NULL,

	CONSTRAINT FK_TAG FOREIGN KEY (tag) REFERENCES tagcommentaire(nomtag),
	CONSTRAINT FK_SOURCE FOREIGN KEY (source) REFERENCES source(url)
	
);

DROP TABLE IF EXISTS ecritsource CASCADE;
CREATE TABLE ecritsource(
	nomauteursource VARCHAR(100),
	urlsource TEXT,
	ecritle DATE NOT NULL DEFAULT CURRENT_DATE,

	PRIMARY KEY(nomauteursource, urlsource),
	CONSTRAINT FK_AUTEUR FOREIGN KEY (nomauteursource) REFERENCES auteursource(nom),
	CONSTRAINT FK_URL FOREIGN KEY (urlsource) REFERENCES source(url)
);
	
DROP TABLE IF EXISTS ecritcommentaire CASCADE;
CREATE TABLE ecritcommentaire(
	nomauteurcommentaire VARCHAR(100),
	titrecommentaire VARCHAR(350),
	commentedate DATE NOT NULL DEFAULT CURRENT_DATE,
	PRIMARY KEY(nomauteurcommentaire,titrecommentaire),
	CONSTRAINT FK_AUTEUR FOREIGN KEY (nomauteurcommentaire) REFERENCES 
	auteurcommentaire(nom),
	CONSTRAINT FK_TITRE FOREIGN KEY (titrecommentaire) REFERENCES
	commentaire(titre)
);

DROP TABLE IF EXISTS refloicomm CASCADE;
CREATE TABLE refloicomm(
	titrecom VARCHAR(350),
	urlloi TEXT,
	phrase TEXT NOT NULL,

	PRIMARY KEY (titrecom, urlloi),
	CONSTRAINT FK_TITRE FOREIGN KEY (titrecom) REFERENCES commentaire(titre),
	CONSTRAINT FK_URL FOREIGN KEY (urlloi) REFERENCES lienlois(url)
);

DROP TABLE IF EXISTS resNLP CASCADE;
CREATE TABLE resNLP(
	titrecomm VARCHAR(350) PRIMARY KEY,
	personalitepolitique VARCHAR(150),
	lieu VARCHAR(100),

	CONSTRAINT FK_TITRE FOREIGN KEY (titrecomm) REFERENCES commentaire(titre)
);

