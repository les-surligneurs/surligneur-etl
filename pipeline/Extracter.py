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
        for  lien in  all_url :
            if lien.h1 != None : 

                page = BeautifulSoup(self.get_page(lien.get('href')), 'html5lib' )
                articles = page.find_all ("div", {"class": "row"},)

                for article in articles:
                    child = article
                    
                    if child.find("div", {"class": "texte"} ) != None : 
                        Extracted = []
                        #print("URL : ")
                        URL  = lien.get('href')
                        Extracted.append(URL)
                        #print ("\33[93m"+URL+Style.RESET_ALL)
                        
                        
                        #print ("Titre :")
                        child = child.parent.parent 
                        TITRE = clear_text (str (child.find('h1')) )
                        Extracted.append(TITRE)
                        #print ("\33[93m" +TITRE+Style.RESET_ALL)
                        
                        
                        
                        #print ("Sous titre :")
                        SUBTITRE = clear_text (str (child.h2))
                        #print ("\33[93m" +SUBTITRE+Style.RESET_ALL)
                        Extracted.append(SUBTITRE)

                        #print ("Auteur  :"  )
                        tokens =  clear_text (str (child.h2)).split("//")
                        final = []
                        AuteursArticles = []
                        for element in tokens: 
                            final.append( element.split(","))
                        for element in final :
                            #print (" :>  " +"\33[93m" + str ( element[0])+Style.RESET_ALL)
                            AuteursArticles.append( str(element[0]))
            
                        Extracted.append(AuteursArticles)
                        
                        ProfessionAuteursArticles = []
                        #print("Profession : ")
                        for element in final : 
                                try:
                                    if ( any(char.isdigit() for char in element[1] ) == False ):
                                        #print (" :>  " +"\33[93m" + str ( element[1])+Style.RESET_ALL)
                                        ProfessionAuteursArticles.append(str ( element[1]))
                                    else:
                                        #Exemple RMC SPORT  28 JUILLET BALALA 
                                        #print(" :>  "+"\33[93m" +"Média"+Style.RESET_ALL)
                                        ProfessionAuteursArticles.append("Média")
                                except  IndexError:
                                    continue    

                        Extracted.append(ProfessionAuteursArticles)
                        
                        #print ("Date Article :")
                        data = re.search(r'[0-9]*[0-9] [a-z]+ [0-9]*[0-9]*[0-9]*[0-9]*',clear_text (str (child.h2)))
                        try:
                            #print(" :>  " + "\33[93m" + data.group(0)+Style.RESET_ALL)
                            DatePublicationArticle = data.group(0)
                            Extracted.append (DatePublicationArticle)
                        except AttributeError:
                            #print(" :>  "+"\33[93m"+"autre type d'article"+Style.RESET_ALL)
                            continue
                        
                        try :
                            #print ("Catégorie :")
                            #print (" :>  " +"\33[93m"+clear_text (str  (child.find("button", {"class": "etiquette"})))+Style.RESET_ALL)
                            Category = clear_text (str  (child.find("button", {"class": "etiquette"})))
                        except AttributeError : 
                            #print(" :>  "+"\33[93m"+"Balise catégorie non trouvé !"+Style.RESET_ALL)
                            Category = None 
                          
                       
                        Extracted.append (Category)
                        AuteursCommentaire = []
                        try :
                            #print ("Détailles auteurs commentaire:"  )     
                            #print (" :>  " +"\33[93m"+clear_text (str (child.find ("div" , {"class" : "auteur"} )))+Style.RESET_ALL)
                            #print ("Auteur Commentaire:"  )
                            # si ya plusieurs auteures on aura  auteur1 , profession // auteur2  , profession etc
                            tokens = clear_text (str (child.find ("div" , {"class" : "auteur"} ))).split("//")
                            final = []
                            for element in tokens: 
                                final.append( element.split(","))
                            for element in final : 
                                #print (" :>  "+"\33[93m" + str ( element[0])+Style.RESET_ALL)
                                AuteursCommentaire.append (element[0])
                                
                            ProfessionAuteursCommentaire = []
                            #print("Profession auteur : ")
                            for element in final : 
                                try:
                                    #print (" :>  " +"\33[93m" + str ( element[1])+Style.RESET_ALL)
                                    ProfessionAuteursCommentaire.append(element[1])
                                except  IndexError:
                                    continue
                            #print ("Date Commentaire : ")
                           
                            data = re.search(r'[0-9]*[0-9] [a-z]+ [0-9]*[0-9]*[0-9]*[0-9]*',clear_text (str (child.find ("div" , {"class" : "auteur"} ))))
                            #print (" :>  " +"\33[93m" +data.group(0)+Style.RESET_ALL)
                            DateCommentaire = data.group(0)
                        except AttributeError : 
                            #print("\33[93m" +"balise Auteur non trouvé! "+Style.RESET_ALL)
                            continue
                        
                        
                        Extracted.append (AuteursCommentaire)
                        Extracted.append (ProfessionAuteursCommentaire)
                        Extracted.append (DateCommentaire)
                        try :
                            #print("\n")
                            #print ("Commentaire :")
                            #print ("\33[93m" + clear_text (str (child.find ("div" , {"class" : "correction"})))+Style.RESET_ALL)
                            Commentaire = clear_text (str (child.find ("div" , {"class" : "correction"})))
                        except AttributeError : 
                            #print("\33[93m" +"Balise Commentaire non trouvé !"+Style.RESET_ALL)
                            continue

                        Extracted.append (Commentaire)

                        Corps =(child.find ("div" , {"class" : "texte"} ))
                        text = str (clear_text(str (Corps)))
                        ArSuggRcours=[]
                        liensverslois=[]
                        ArSuggNoRcours = []
                        for paragraphe in Corps.find_all('p'):

                            if (">LIRE:")  in str (paragraphe) :
                                #print("******* Paragraphe contenant des articles à suggérer en relation avec l'article en cours *******")
                                for m in paragraphe.find_all('a'):
                                    #print ( "\33[93m" + "URL  article  :    "   + str (m.get('href'))  + Style.RESET_ALL)
                                    #print ( "\33[93m" + "Data article  :    " + clear_text (str(m))  + Style.RESET_ALL)
                                    ArSuggRcours.append( str (m.get('href')))
                                    ArSuggRcours.append(clear_text (str(m)))
                                   
                            
                            if ("À LIRE ") not in str (paragraphe): 
                                data =  paragraphe.find_all('a')
                                if (len(data) > 0):
                                    #print("******* Paragraphe contenant des liens vers des lois  *******")
                                    pass
                                
                                for m in data:
                                    #print ( "\33[93m" + "URL   loi  :    "   + str (m.get('href'))  + Style.RESET_ALL)
                                    #print ( "\33[93m" + "Text  Gras :    " + clear_text (str(m))  + Style.RESET_ALL)
                                    liensverslois.append(str (m.get('href')))
                                    liensverslois.append (clear_text (str(m)))

                            else:
                                #print( "********Paragraphe contenant des liens des article à suggérer sans  aucune relation ********")
                                for m in paragraphe.find_all('a'):
                                    #print ( "\33[93m" + "URL  article  :    "   + str (m.get('href'))  + Style.RESET_ALL)
                                    #print ( "\33[93m" + "Data article  :    " + clear_text (str(m))  + Style.RESET_ALL)
                                    ArSuggNoRcours.append (str (m.get('href')))
                                    ArSuggNoRcours.append (clear_text (str(m)))
                        
                        
                        
                        Extracted.append (text)
                        Extracted.append (ArSuggRcours)
                        Extracted.append (liensverslois)
                        Extracted.append (ArSuggNoRcours)

                        
                        cpt += 1
                        Extracted_All.append(Extracted)
        
        print ("\33[93m" + "nombre d'articles total scraper : " +  str(cpt) +Style.RESET_ALL )
        return Extracted_All 



if __name__ == '__main__':

      
    Scrapper = Extracter ()
    listes_Articles = Scrapper.get_articles()
    
    for a in listes_Articles[6] : 
        print (a)
        print ( "\33[93m" +"***************************************************************************************" + Style.RESET_ALL)

    print ("\33[93m" + "la liste contient " + str (len(listes_Articles)) + " articles "+Style.RESET_ALL)
    



