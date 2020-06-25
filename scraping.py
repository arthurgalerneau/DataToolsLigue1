# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:14:40 2020

@author: thomas, armand, arthur
"""

from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium import webdriver



domiciles=[]
exterieurs=[]
scoredoms=[]
scoreexts=[]
resultats=[]
saisons=[]


for x in range(4,9) :

    driver=webdriver.Chrome(r"C:\Users\Actif\Documents\chromedriver")
    y=x+1
    driver.implicitly_wait(1)
    url= 'https://www.flashscore.fr/football/france/ligue-1-201'+str(x)+'-201'+str(y)+'/resultats/'
    driver.get(url)
    
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(5)
    Accept_button = soup.find('button', attrs={'id' :"onetrust-accept-btn-handler"})

    string = '$("#'+Accept_button.get('id')+'").click();'
    driver.execute_script(string)
    
    more_matchs = driver.find_element_by_partial_link_text('Montrer plus de matchs')
    present = True
    while present == True :
        time.sleep(5)
        try :
            more_matchs.click()
            print("click")
        except:
            present = False
            print("error")
        
    
    time.sleep(5)
    soup1 = BeautifulSoup(driver.page_source,'html.parser')
    liste_matchs=soup1.find_all('div',class_=re.compile("event__match event__match--static"))
    print(len(liste_matchs))
   
    for i in liste_matchs :
        saison="201"+str(x)+"-201"+str(y)
        
        domicile=i.find('div',class_=re.compile("event__participant event__participant--home"))
        domicile=domicile.text
         
        exterieur=i.find('div',class_=re.compile("event__participant event__participant--away"))
        exterieur=exterieur.text
        
        score=i.find('div', class_="event__scores fontBold")
        scoredom=score.span.text
        scoreext=score.span.next_sibling.next_sibling.text
        
        scoredom=int(scoredom)
        scoreext=int(scoreext)
        
        if scoredom > scoreext :
            resultat="VD"
        if scoredom < scoreext :
            resultat="VE"
        if scoredom == scoreext :
            resultat="N"
        
        domiciles.append(domicile)
        exterieurs.append(exterieur)
        scoredoms.append(scoredom)
        scoreexts.append(scoreext)
        resultats.append(resultat)
        saisons.append(saison)
        
     
        #print(domicile+" "+str(scoredom)+" "+exterieur+" "+str(scoreext))
    driver.close()
    
    
    



matchs=pd.DataFrame({
    'saison':saisons,
    'equipe_dom':domiciles,
    'equipe_ext':exterieurs,
    'score_dom':scoredoms,
    'score_ext':scoreexts,
    'resultat':resultats})




matchs.to_csv(r'resultats_matchs.csv',sep=";",index=None)

