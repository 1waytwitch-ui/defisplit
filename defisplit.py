import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io

# Configuration de la page
st.set_page_config(page_title="Analyse de Portefeuille", layout="wide")

# Titre
st.title("📊 Analyse de Portefeuille Crypto / DeFi")
st.markdown("Suivez vos investissements par **catégorie** (LP, staking, REALT, etc.) et analysez leur évolution.")

# Disclaimer
with st.expander("ℹ️ À propos des données"):
    st.info("⚠️ **Les données que vous saisissez sont stockées uniquement dans votre navigateur (via `session_state`) et ne sont ni sauvegardées ni envoyées sur un serveur distant.**\n\nPour garder une trace, vous pouvez exporter le fichier CSV en local.")

# Initialisation des catégories
if "categories" not in st.session_state:
    st.session_state.categories = ["LP", "AAVE"]

# Barre latérale : Ajouter une nouvelle catégorie
st.sidebar.header("➕ Ajouter une catégorie")
new_cat = st.sidebar.text_input("Nom de la catégorie")
if st.sidebar.button("Ajouter"):
    new_cat = new_cat.strip().upper()
    if new_cat and new_cat not in st.session_state.categories:
        st.session_state.categories.append(new_cat)
    elif new_cat in st.session_state.categories:
        st.sidebar.warning("Catégorie déjà présente.")
    else:
        st.sidebar.warning("Veuillez entrer un nom valide.")

# Entrée des montants
st.subheader("💰 Données par catégorie")
initial_values = []
actual_values = []

with st.form("formulaire_investissements"):
    cols = st.columns([2, 2, 2])
    cols[0].markdown("**Catégorie**")
    cols[1].markdown("**Montant initial ($)**")
    cols[2].markdown("**Montant actuel ($)**")

    for cat in st.session_state.categories:
        col1, col2, col3 = st.columns([2, 2, 2])
        col1.text(cat)
        initial = col2.number_input(f"Initial_{cat}", label_visibility="collapsed", min_value=0.0, value=0.0, step=100.0)
        actuel = col3.number_input(f"Actuel_{cat}", label_visibility="collapsed", min_value=0.0, value=0.0, step=100.0)
        initial_values.append(initial)
        actual_values.append(actuel)

    submitted = st.form_submit_button("📈 Mettre à jour l'analyse")

# Traitement si des données sont valides
if sum(initial_values) > 0 and sum(actual_values) > 0:
    df = pd.DataFrame({
        "Catégorie": st.session_state.categories,
        "Initial ($)": initial_values,
        "Actuel ($)": actual_values,
    })

    df["% Initial"] = df["Initial ($)"] / df["Initial ($)"].sum() * 100
    df["% Actuel"] = df["Actuel ($)"] / df["Actuel ($)"].sum() * 100
    df["ROI (%)"] = (df["Actuel ($)"] - df["Initial ($)"]) / df["Initial ($)"] * 100

    # Affichage tableau
    st.subheader("📋 Résumé de l'analyse")
    st.dataframe(df.round(2), use_container_width=True)

    # Bouton d'export CSV
    st.download_button(
        label="💾 Exporter au format CSV",
        data=df.round(2).to_csv(index=False).encode('utf-8'),
        file_name="analyse_portefeuille.csv",
        mime="text/csv"
    )

    # Graphiques
    st.subheader("📊 Répartition du portefeuille")

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].pie(df["% Initial"], labels=df["Catégorie"], autopct='%1.1f%%', startangle=90)
    axs[0].set_title("Répartition Initiale")

    axs[1].pie(df["% Actuel"], labels=df["Catégorie"], autopct='%1.1f%%', startangle=90)
    axs[1].set_title("Répartition Actuelle")

    plt.tight_layout()
    st.pyplot(fig)

else:
    st.info("Veuillez entrer des montants initiaux et actuels pour afficher l'analyse.")

# Footer
st.markdown("---")
st.markdown("🛠️ *Application créée avec Streamlit pour suivre votre portefeuille crypto et DeFi. Ajoutez des catégories comme LP, staking, REALT, etc.*")
