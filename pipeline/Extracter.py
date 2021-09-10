from logging import fatal
from types import new_class
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Back, Style,init


init(convert=True)


"""
    # Formatte le code html d'un objet en supprimant ses balises html
    # @param raw_html code html à formatter
    # @return le code html sans les balises html
"""
def clear_text(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Extracter:
    """
        # Constructeur  qui initialise l'url par le site web des surligneurs
    """
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/'
    """
        # Permet de récupérer le contenu d'une page web au format objet HTML interprétable par python
        # @param  url  lien de la page à récupérer
        # @return le resulat d'une requete web sous format HTML
    """
    def get_page(self, url):
        response = requests.request('GET', url)
        if not response.ok:
            print('Erreur dans le téléchargement de la page' + str(url))
        content = response.content.decode('utf-8')
        return content
    
    """
        # Permet de récupérer tous les liens contenu dans un objet html
        # @param html_page objet html sur lequel on cherchera les liens
        # @return tous les liens d'une page html 
    """
    def get_url(self , html_page):
        soup = BeautifulSoup(self.get_page(html_page), 'lxml')
        return soup.find_all('a')
    
    """
        # Récupére les articles et leurs informations contenus dans un objet html 
        # @return  toutes les informations concernant un ou plusieurs article(s) sous forme de liste
    """
    def get_articles(self):
        #liste qui va contenir tout les articles 
        Extracted_All =[]
        #on récupère tout les urls et on les regarde  1 par 1 
        all_url = self.get_url(self.url)
        cpt = 0
        tr = set ()
        for  lien in  all_url :
             #si le lien possede un titre cest que cest une page qui contient des articles sinon ca mene autre pas #pas intéressant
            if lien.h1 != None : 
                page = BeautifulSoup(self.get_page(lien.get('href')), 'html5lib' )
                articles = page.find_all ("div", {"class": "row"},)
                #pour chaque article dans cette page qui contient plusieurs articles
                for article in articles:
                    child = article
                    #liste qui va contenir 1 article a la fin de boucle 
                    Extracted = []

                    if child.find("div", {"class": "texte"} ) != None :

                        URL = lien.get('href')
                        child = child.parent.parent
                        #titre de l'article
                        TITRE = str(clear_text(str(child.find('h1'))))
                        #sous titre 
                        SUBTITRE = clear_text(str(child.h2))
                        #lien de source vers larticle 
                        url_source = child.find("a").get('href')
                        Extracted.append(url_source)
                        Extracted.append(TITRE)
                        Extracted.append(SUBTITRE)
                        tokens =  clear_text (str (child.h2)).split("//")
                        final = []
                        #liste des auteurs 
                        AuteursArticles = []
                        for element in tokens: 
                            final.append( element.split(","))
                        for element in final :
                            AuteursArticles.append( str(element[0]))
            
                        Extracted.append(AuteursArticles)

                        #liste des professions des auteurs de larticle 
                        ProfessionAuteursArticles = []
                        for element in final : 
                                try:
                                    if ( any(char.isdigit() for char in element[1] ) == False ):
                                        ProfessionAuteursArticles.append(str ( element[1]))
                                    else:
                                        ProfessionAuteursArticles.append("Média")
                                except  IndexError:
                                    continue    

                        Extracted.append(ProfessionAuteursArticles)        
                     
                        #date publication article
                        data = re.search(r'[0-9]*[0-9] [a-z]+ [0-9]*[0-9]*[0-9]*[0-9]*',clear_text (str (child.find("h2"))))
                        try:
                            DatePublicationArticle = str (data)
                            tokens = DatePublicationArticle.split(",")
                           
                            if len(tokens) == 3 :
                                DatePublicationArticle = str (tokens[2]).replace( "\'>" ,"")
                                DatePublicationArticle = DatePublicationArticle.split("'")[1]
                            else: 
                                 DatePublicationArticle = " "
                            
                            Extracted.append (DatePublicationArticle)
                        except AttributeError:
                            continue
                        
                        # categorie article 
                        try :
                            Category = clear_text (str  (child.find("button", {"class": "etiquette"})))
                        except AttributeError : 
                            Category = None 
                        Extracted.append (Category)

                        #liste des auteurs du commentaire , liste des professions des auteurs  et la date du commentaire 
                        AuteursCommentaire = []
                        try :

                            tokens = clear_text (str (child.find ("div" , {"class" : "auteur"} ))).split("//")
                            
                            final = []
                            for element in tokens: 
                                final.append( element.split(","))
                            for element in final : 
                                AuteursCommentaire.append (element[0])
                                
                            ProfessionAuteursCommentaire = []
                            
                            for element in final : 
                                try:
                                    ProfessionAuteursCommentaire.append(element[1])
                                except  IndexError:
                                    continue
                            data = re.search(r'[0-9]*[0-9] [a-z]+ [0-9]*[0-9]*[0-9]*[0-9]*',clear_text (str (child.find ("div" , {"class" : "auteur"} ))))
                            
                            DateCommentaire = str (data)
                            tokens = DateCommentaire.split (",")
                            if len(tokens) == 3 :
                                DateCommentaire= str (tokens[2]).replace( "\'>" ,"")
                                DateCommentaire = DateCommentaire.split("'")[1]
                            else: 
                                 DateCommentaire = " "
                           
                        except AttributeError:
                            continue
                        
                        
                        Extracted.append (AuteursCommentaire)
                        Extracted.append (ProfessionAuteursCommentaire)
                        Extracted.append (DateCommentaire)
                        
                      
                        #resume du commentaire
                        try :
                            Commentaire = clear_text (str (child.find ("div" , {"class" : "correction"})))
                        except AttributeError : 
                            continue 
                        Extracted.append (Commentaire)

                        #corps du commentaire 
                        Corps =(child.find ("div" , {"class" : "texte"} ))
                        text = str (clear_text(str (Corps)))
                        ArSuggRcours=[]
                        liensverslois=[]
                        ArSuggNoRcours = []

                        for paragraphe in Corps.find_all('p'):
                            # article de la meme categorie que larticle en cours 
                            if (">LIRE:")  in str (paragraphe) :        
                                for m in paragraphe.find_all('a'):
                                    ArSuggRcours.append( str (m.get('href')))
                                    ArSuggRcours.append(clear_text (str(m)))

                             #article  sans aucune relation avec l'article en cours   
                            if ("À LIRE ") not in str (paragraphe): 
                                data =  paragraphe.find_all('a')    
                                for m in data:
                                    liensverslois.append(str (m.get('href')))
                                    liensverslois.append (clear_text (str(m)))
                            #les liens vers des loi qui sont en relation avec larticle en cours 
                            else:
                                for m in paragraphe.find_all('a'):
                                    ArSuggNoRcours.append (str (m.get('href')))
                                    ArSuggNoRcours.append (clear_text (str(m)))
                               
                        
                        Extracted.append (text)
                        Extracted.append (ArSuggRcours)
                        Extracted.append (liensverslois)
                        Extracted.append (ArSuggNoRcours)
                        
                        # on regarse si larticle  existe dans le set 
                        # si il existe on insere pas 
                        if TITRE not in tr :
                            Extracted_All.append(Extracted) 

                        tr.add (TITRE)
                        
        return Extracted_All

