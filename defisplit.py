import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Titre de l'application
st.title("Analyse de Portefeuille d'Investissement")

st.markdown("Entrez manuellement les données d'investissement pour chaque actif.")

# Liste des investissements
investissements = ["LP", "AAVE"]

# Création des champs de saisie
initial_values = []
actual_values = []

for actif in investissements:
    col1, col2 = st.columns(2)
    with col1:
        initial = st.number_input(f"Montant initial pour {actif} ($)", min_value=0.0, value=0.0, step=100.0)
    with col2:
        actuel = st.number_input(f"Montant actuel pour {actif} ($)", min_value=0.0, value=0.0, step=100.0)
    
    initial_values.append(initial)
    actual_values.append(actuel)

# Création du DataFrame
df = pd.DataFrame({
    "Investissement": investissements,
    "Initial ($)": initial_values,
    "Actuel ($)": actual_values,
})

# Vérifier si les totaux sont non nuls pour éviter la division par zéro
if df["Initial ($)"].sum() == 0 or df["Actuel ($)"].sum() == 0:
    st.warning("Veuillez entrer des montants supérieurs à zéro pour afficher les graphiques et l'analyse.")
else:
    # Calculs
    total_initial = df["Initial ($)"].sum()
    total_actuel = df["Actuel ($)"].sum()
    
    df["% Initial"] = df["Initial ($)"] / total_initial * 100
    df["% Actuel"] = df["Actuel ($)"] / total_actuel * 100
    df["ROI (%)"] = (df["Actuel ($)"] - df["Initial ($)"]) / df["Initial ($)"] * 100

    # Affichage du tableau
    st.subheader("Tableau d'analyse")
    st.dataframe(df.round(2))

    # Création des graphiques
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Graphique 1 : Répartition initiale
    axs[0].pie(df["% Initial"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
    axs[0].set_title("Répartition Initiale (%)")

    # Graphique 2 : Répartition actuelle
    axs[1].pie(df["% Actuel"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
    axs[1].set_title("Répartition Actuelle (%)")

    plt.tight_layout()

    # Affichage du graphique
    st.subheader("Visualisation des Répartitions")
    st.pyplot(fig)
