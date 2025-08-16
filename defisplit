import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Titre de l'application
st.title("Analyse de Portefeuille d'Investissement")

# Données de départ
data = {
    "Investissement": ["LP", "AAVE"],
    "Initial ($)": [15000, 1900],
    "Actuel ($)": [12000, 11230],
}

# Création du DataFrame
df = pd.DataFrame(data)

# Calcul des totaux
total_initial = df["Initial ($)"].sum()
total_actuel = df["Actuel ($)"].sum()

# Calculs supplémentaires
df["% Initial"] = df["Initial ($)"] / total_initial * 100
df["% Actuel"] = df["Actuel ($)"] / total_actuel * 100
df["ROI (%)"] = (df["Actuel ($)"] - df["Initial ($)"]) / df["Initial ($)"] * 100

# Affichage du DataFrame arrondi
st.subheader("Tableau d'analyse")
st.dataframe(df[["Investissement", "Initial ($)", "Actuel ($)", "% Initial", "% Actuel", "ROI (%)"]].round(2))

# Création des graphiques
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Graphique 1 : Répartition initiale
axs[0].pie(df["% Initial"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
axs[0].set_title("Répartition Initiale (%)")

# Graphique 2 : Répartition actuelle
axs[1].pie(df["% Actuel"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
axs[1].set_title("Répartition Actuelle (%)")

plt.tight_layout()

# Affichage des graphiques dans Streamlit
st.subheader("Visualisation des Répartitions")
st.pyplot(fig)
