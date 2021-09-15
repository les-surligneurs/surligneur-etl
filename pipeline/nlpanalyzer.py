import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize


nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')
french_stopwords = set(stopwords.words('french'))


"""
# 
"""
class nlpanalyzer:

    def __init__(self):
        pass
    """
        # Extrait à partir d'une chaîne de caractère un nom et un prénom supposé
        # @param titre la chaîne de caractère a analyser en l'occurence le titre
        # @return string le prénom et nom dans le titre ou Aucun sinon
    """
    def extractNamefromtitle(self,titre: str):
        french_stopwords = set(stopwords.words('french'))
        token = word_tokenize(titre, language="french")
        cleaneddata = [w for w in token if not w.lower() in french_stopwords]
        Tokennamed = nltk.pos_tag(cleaneddata)
        parsed = nltk.RegexpParser('exact: {<JJR><NNP>||<NNP><NNP>||<JJ><NNP>}').parse(Tokennamed)
        resultat = "Aucun"
        for data in parsed:
            if re.search("exact", str(data)):
                resultat = data
                break
        dictionaire = {"exact": "", "/JJR": "", "/NNP": "", ")": "", "(": "", "/JJ": ""}
        for k, v in dictionaire.items():
            resultat = str(resultat).replace(k, v)
        return resultat

    """
        # Extrait à partir d'une chaîne de caractère le lieu trouvé
        # @param titre la chaîne de caractère a analyser en l'occurence le titre
        # @return string Le lieu trouvé dans le titre ou Aucun sinon
    """
    def extractPlacefromtitle(self, titre: str) -> str:
        french_stopwords = set(stopwords.words('french'))
        token = word_tokenize(titre, language="french")
        cleaneddata = [w for w in token if not w.lower() in french_stopwords]
        Tokennamed = nltk.pos_tag(cleaneddata)
        parsed = nltk.RegexpParser('exact: {<NN>}').parse(Tokennamed)
        resultat = "Aucun"
        for data in parsed:
            if re.search(r'exact [A-ZÀ-Ö][A-Za-zÀ-ÖØ-öø-ÿ-]+', str(data)):
                resultat = data
                break
        dictionaire = {"exact": "", "/NN": ""}
        for k, v in dictionaire.items():
            resultat = str(resultat).replace(k, v)
        return resultat
