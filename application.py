# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:46:47 2020

@author: thomas, armand, arthur
"""

from tkinter import *
from tkinter.filedialog import *
import shutil, os, csv
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

df = pd.read_csv("resultats_matchs.csv", delimiter=";", )

list_equipe = df.drop_duplicates(subset='equipe_dom', keep="last")['equipe_dom'].values

screen = Tk()
screen.geometry("500x375")
screen.title("Analyse des equipes de Ligue 1")

L1 = Label(screen, text="Nom de l'equipe")
L1.pack(side = TOP)
E1 = Entry(screen, bd =5)
E1.pack(side = TOP)
matplotlib.use('TkAgg')


def evolution_saison(df):
    equipe_choix = E1.get()
    df = df[(df['equipe_dom'] == equipe_choix )|(df['equipe_ext'] == equipe_choix)]
    analyse = pd.DataFrame(columns=['score'], index=df.drop_duplicates(subset='saison', keep='last')['saison'].values)
    analyse.loc[:,'score'] = 0
    for saison,equipe_dom, equipe_ext, resultat in df[['saison','equipe_dom','equipe_ext','resultat']].values.tolist()  :
        if (equipe_dom == equipe_choix) & (resultat == "VD") :
            analyse.loc[saison,'score'] += 3 
        if (equipe_dom == equipe_choix) & (resultat == "N") :
            analyse.loc[saison,'score'] += 1
        if (equipe_ext == equipe_choix) & (resultat == "N") :
            analyse.loc[saison,'score'] += 1
        if (equipe_ext == equipe_choix) & (resultat == "VE") :
            analyse.loc[saison,'score'] += 3 

    f = plt.figure(figsize=(20,10))
    plt.title("Evolution de "+equipe_choix+" par saison")
    plt.plot(analyse.index, analyse['score'], label="évolution du score")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel("Saison")
    plt.ylabel("Score")
    f.canvas.draw()
    matplotlib.use('TkAgg')
    
    
    
    

def evolution_nombre_but(df):
    equipe_choix = E1.get()
    df = df[(df['equipe_dom'] == equipe_choix )|(df['equipe_ext'] == equipe_choix)]
    analyse = pd.DataFrame(columns=['but_enc','but_mark'], index=df.drop_duplicates(subset='saison', keep='last')['saison'].values)
    analyse.loc[:,'but_enc'] = 0
    analyse.loc[:,'but_mark'] = 0
    for saison,equipe_dom, equipe_ext, score_ext,score_dom in df[['saison','equipe_dom','equipe_ext','score_ext','score_dom']].values.tolist() : 
        if (equipe_dom == equipe_choix) :
            analyse.loc[saison,'but_enc']  += score_ext
            analyse.loc[saison,'but_mark'] += score_dom
        if (equipe_ext == equipe_choix) :
            analyse.loc[saison,'but_enc']  += score_dom
            analyse.loc[saison,'but_mark'] += score_ext
    f = plt.figure(figsize=(20,10))
    plt.title("Evolution des buts de "+equipe_choix)
    plt.plot(analyse.index, analyse['but_enc'], label="évolution des buts encaissés")
    plt.plot(analyse.index, analyse['but_mark'], label="évolution des buts marqués")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel("Saison")
    plt.ylabel("Nombre de buts encaissés/marqués")
    f.canvas.draw()

    
def evolution_match_VD(df):
    equipe_choix = E1.get()
    df = df[(df['equipe_dom'] == equipe_choix )|(df['equipe_ext'] == equipe_choix)]
    analyse = pd.DataFrame(columns=['victoire','defaite','egalite'], index=df.drop_duplicates(subset='saison', keep='last')['saison'].values)
    analyse.loc[:,'victoire'] = 0
    analyse.loc[:,'defaite'] = 0
    analyse.loc[:,'egalite'] = 0
    for saison,equipe_dom, equipe_ext,resultat in df[['saison','equipe_dom','equipe_ext','resultat']].values.tolist() : 
        if (equipe_dom == equipe_choix):
            if (resultat == "VD"):
                analyse.loc[saison,'victoire']  += 1
            else:
                analyse.loc[saison,'defaite']  += 1
        if (equipe_ext == equipe_choix):
            if (resultat == "VE"):
                analyse.loc[saison,'victoire']  += 1
            else:
                analyse.loc[saison,'defaite']  += 1
        if (resultat == "N") :
            analyse.loc[saison,'egalite']  += 1
            
    f = plt.figure(figsize=(20,10))
    plt.title("Evolution des matchs de "+equipe_choix)
    plt.plot(analyse.index, analyse['victoire'], label="évolution des victoires")
    plt.plot(analyse.index, analyse['defaite'], label="évolution des defaites")
    plt.plot(analyse.index, analyse['egalite'], label="évolution des égalités")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel("Saison")
    plt.ylabel("Nombre de V/D")
    f.canvas.draw()
     
    

bouton1 = Button(screen, text ="Evolution des points", relief=GROOVE, width=100, height=5, command= partial(evolution_saison, df)).pack()
bouton2 = Button(screen, text ="Evolution des butes", relief=GROOVE, width=100, height=5, command= partial(evolution_nombre_but, df)).pack()
bouton3 = Button(screen, text ="Evolution des victoires/defaites", relief=GROOVE, width=100, height=5, command= partial(evolution_match_VD, df)).pack()

Label(screen, text="Arthur GALERNEAU - Armand DUSART - Thomas HANDSHUMACHER").pack(anchor="center", padx=5, pady=5)

screen.mainloop()