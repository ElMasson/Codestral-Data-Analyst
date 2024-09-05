import streamlit as st
import pandas as pd
import os
from main import describe_and_analyze_file
import matplotlib.pyplot as plt


# Configuration de l'interface utilisateur
st.set_page_config(page_title="Codestral Data Analyst", layout="wide")

# Réduire la taille du logo de 50% et ajouter un titre
# Réduire la taille du logo de 50% et ajouter un titre
st.sidebar.image('img/DUKE Logo.png', use_column_width=True)
st.sidebar.markdown(
    """
    <h1 style='text-align: center;'>Codestral Data Analyst</h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Configuration")
file_uploaded = st.sidebar.file_uploader("Choisissez un fichier Excel", type=['xls', 'xlsx'])

# Affichage des fichiers disponibles dans le dossier /data
st.sidebar.subheader("Fichiers disponibles")
data_files = [f for f in os.listdir('data') if f.endswith(('.xls', '.xlsx'))]
selected_file = st.sidebar.selectbox("Sélectionnez un fichier disponible", options=data_files)

# Fonction pour afficher les premières lignes des données
def display_first_rows(file_path):
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        st.subheader(f"Feuille: {sheet_name}")
        df = pd.read_excel(xls, sheet_name)
        st.dataframe(df.head())

# Si un fichier est téléchargé, l'enregistrer dans le dossier /data
if file_uploaded:
    file_path = os.path.join('data', file_uploaded.name)
    with open(file_path, "wb") as f:
        f.write(file_uploaded.getbuffer())
    st.sidebar.success(f"Fichier {file_uploaded.name} téléchargé avec succès.")
    selected_file = file_uploaded.name  # Mettre à jour le fichier sélectionné

if selected_file:
    file_path = os.path.join('data', selected_file)

    # Afficher les premières lignes des données dès le choix du fichier
    with st.expander("Afficher les premières lignes du fichier", expanded=True):
        display_first_rows(file_path)

    # Question de l'utilisateur pour l'analyse
    st.sidebar.subheader("Analyse des données")
    user_question = st.sidebar.text_input("Posez ici votre question", value="")

    if st.sidebar.button("Analyser"):
        with st.spinner("Analyse en cours..."):
            try:
                analysis_code = describe_and_analyze_file(file_path, user_question)

                # Affichage du code de l'analyse dans une section repliable
                with st.expander("Afficher le code"):
                    st.code(analysis_code, language='python')

                # Réduire la taille du graphique de 20%
                fig = plt.gcf()
                fig.set_size_inches(fig.get_size_inches() * 0.75)

                # Affichage du graphique généré par matplotlib
                st.pyplot(fig)  # Utilise fig pour obtenir le graphique courant


            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")

else:
    st.sidebar.info("Téléchargez un fichier Excel ou sélectionnez un fichier disponible pour commencer l'analyse.")
