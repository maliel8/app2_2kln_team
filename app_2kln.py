import streamlit as st
import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
import joblib

## fonction pour transformer mes donnees 
def normaliser(genre, niveaux_etude_parent, dejeuner, cours_repetition):
   
    if genre == 'female':
        genre_ = 0
    else:
        genre_ = 1

    niveaux_etude_mapping = {
        "BEPC": 1,
        "Bac": 2,
        "BAC + 1": 3,
        "BTS": 4,
        "LICENCE": 5,
        "MASTER": 6
    }
    niveaux = niveaux_etude_mapping.get(niveaux_etude_parent, 6)

    dejeuner_mapping = {
        "normal": 1,
        "reduit": 0
    }
    dejeuner_ = dejeuner_mapping.get(dejeuner, 1)  # Default to normal (1)

    cours_repetition_mapping = {
        "non": 0,
        "oui": 1
    }
    repetition = cours_repetition_mapping.get(cours_repetition, 0)  # Default to non (0)

    return genre_, niveaux, dejeuner_, repetition

#fonction pour recuperer les inforamation de l'etudiant 
def student_info():
    genre = st.sidebar.radio(
        "selectioner votre genre",
        ("male" , "female")
        )
    niveaux_etude_parent = st.sidebar.selectbox(
        "quel est niveaux d'etude de vos parent",
        
        ("BEPC","Bac","BAC + 1","BTS","LICENCE","MASTER")
        ) 
    dejeuner 	= st.sidebar.radio(
        "quel type dejeuner prennez vous  ",

        ("normale","reduit")
        )
    cours_repetition =st.sidebar.radio(
        "faitez vous des cours de remise a niveaux",

        ("non","oui"
            )
        )
    genre, niveaux_etude, dejeuner, repetition  = normaliser(genre, niveaux_etude_parent, dejeuner, cours_repetition)
    donnee_user = {
    'genre': genre,	
    'niveaux_etude_parent': niveaux_etude,
    'dejeuner' 	: dejeuner,
    'cours_repetition':repetition
    }


    return donnee_user



st.title('''BIENVENUE SUR PREDIT_RESULTAT''')
st.write('''
   une application qui permet aux etudiants de savoir s'ils vont validees leurs EU(matieres) ou non
         et qui les prodigues les conseiles pour s'ameliorer
''')

st.sidebar.header("Formulaire D'enquete")


donnee_entre = student_info() 
donnee_pred = pd.DataFrame(donnee_entre,index = [1])  

st.sidebar.write("afficher les donnees")                  
bt = st.sidebar.button('afficher')

if(bt == True):
    st.title('Donnees')
    st.write(donnee_pred)


# Chargez le modèle à partir du fichier .joblib
ref = joblib.load('model_ref1.joblib')
pred = st.sidebar.button('executer')
     
if(pred == True):
    predict =  ref.predict(donnee_pred)
        # Utilisez le modèle chargé pour faire des prédictions
    st.subheader("........................prediction.....................")
    if(predict == 1):
        st.write(" ### vous avez 50.0% de chance de reussir")
    elif(predict == 0):
        st.write("## vous avez 99.99% de chance d'echouer")
    else:
      st.write("### brovor!! vous avec 99.99% de chance de reussir")
    st.title('CONSEIL PRATIQUE')
    if(predict == 0 | predict == 1):
            if(donnee_entre['cours_repetition'] ==0 & donnee_entre['dejeuner'] == 0):
                st.write('''### faite des cours de remise a niveau et 
                            ### changez votre alimentation 
                        ''')

            elif(donnee_entre['cours_repetition']  ==0 & donnee_entre['dejeuner']==1):
                st.write(''' 
                        ### faite des cours de remise a niveau 
                        ''')

            elif(donnee_entre['cours_repetition']  ==1 & donnee_entre['dejeuner']==0):
                st.write('''
                        ### changez votre alimentation
                        ''')
            else:
                st.write('''
                        ### vous devez doublé d'effort 
                        ''')

    else:
            st.write('''
                    ### excelant !! continué ainsi
                    ''')
    
st.sidebar.caption("by 2KLN_TEAM")