from logging import fatal
from types import new_class
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Back, Style,init
init(convert=True)

def clear_text(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Extracter:
    
    def __init__(self):
        self.url = 'https://lessurligneurs.eu/'

    def get_page(self, url):
        response = requests.request('GET', url)
        if not response.ok:
            print('Erreur dans le téléchargement de la page' + str(url))
        content = response.content.decode('utf-8')
        return content
    

    def get_url(self , html_page):
        soup = BeautifulSoup(self.get_page(html_page), 'lxml')
        return soup.find_all('a')


    def get_articles(self,html_page = ''):
        Extracted_All =[]

        all_url = self.get_url(self.url)
        cpt = 0
        tr = set ()
        for  lien in  all_url :
            if lien.h1 != None : 
                page = BeautifulSoup(self.get_page(lien.get('href')), 'html5lib' )
                articles = page.find_all ("div", {"class": "row"},)
                
                for article in articles:
                    child = article
                    Extracted = []

                    if child.find("div", {"class": "texte"} ) != None : 
            
                        URL  = lien.get('href')
                        Extracted.append(URL)
                        
                        child = child.parent.parent 
                        TITRE = str (clear_text (str (child.find('h1')) ))
                        
                         
                                      
            
                        Extracted.append(TITRE)
                
                        SUBTITRE = clear_text (str (child.h2))
                        Extracted.append(SUBTITRE)

                        tokens =  clear_text (str (child.h2)).split("//")
                        final = []
                        AuteursArticles = []
                        for element in tokens: 
                            final.append( element.split(","))
                        for element in final :
                            AuteursArticles.append( str(element[0]))
            
                        Extracted.append(AuteursArticles)
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
                        

                        try :
                            
                            Category = clear_text (str  (child.find("button", {"class": "etiquette"})))
                            
                        except AttributeError : 
                            Category = None 
                          
                       
                        Extracted.append (Category)
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
                        
                      
                    

                        try :
                            Commentaire = clear_text (str (child.find ("div" , {"class" : "correction"})))
                         
                        except AttributeError : 
                            continue

                        Extracted.append (Commentaire)

                        Corps =(child.find ("div" , {"class" : "texte"} ))
                        text = str (clear_text(str (Corps)))
                        ArSuggRcours=[]
                        liensverslois=[]
                        ArSuggNoRcours = []

                        for paragraphe in Corps.find_all('p'):
                            if (">LIRE:")  in str (paragraphe) :
                                
                                for m in paragraphe.find_all('a'):
                                    ArSuggRcours.append( str (m.get('href')))
                                    ArSuggRcours.append(clear_text (str(m)))

                               
                            if ("À LIRE ") not in str (paragraphe): 
                                data =  paragraphe.find_all('a')    
                                for m in data:
                                    liensverslois.append(str (m.get('href')))
                                    liensverslois.append (clear_text (str(m)))
                                

                            else:
                                for m in paragraphe.find_all('a'):
                                    ArSuggNoRcours.append (str (m.get('href')))
                                    ArSuggNoRcours.append (clear_text (str(m)))
                               
                        
                    
                        Extracted.append (text)
                        Extracted.append (ArSuggRcours)
                        Extracted.append (liensverslois)
                        Extracted.append (ArSuggNoRcours)
                        
                        if TITRE not in tr :
                            Extracted_All.append(Extracted) 

                        tr.add (TITRE)
                        
                        
                        
                        

                        
                        
                    
                        
                            
        print("nombre d'articles scrapper :   " + str (len(Extracted_All)))
        return Extracted_All

