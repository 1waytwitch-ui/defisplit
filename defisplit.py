import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Portefeuille Crypto", layout="wide")

# Titre
st.title("📈 Analyse de Portefeuille Crypto & DeFi")
st.markdown("Ajoutez vos investissements manuellement et suivez leur évolution.")

# Initialisation de session state
if "assets" not in st.session_state:
    st.session_state.assets = ["LP", "AAVE"]

# Barre latérale : Ajouter un nouvel actif
st.sidebar.header("➕ Ajouter un actif")
new_asset = st.sidebar.text_input("Nom de l'actif")
if st.sidebar.button("Ajouter"):
    new_asset = new_asset.strip().upper()
    if new_asset and new_asset not in st.session_state.assets:
        st.session_state.assets.append(new_asset)
    elif new_asset in st.session_state.assets:
        st.sidebar.warning("Actif déjà présent.")
    else:
        st.sidebar.warning("Veuillez entrer un nom valide.")

# Création du tableau dynamique de saisie
st.subheader("💰 Données d'investissement")
initial_values = []
actual_values = []

with st.form("investment_form"):
    cols = st.columns([2, 2, 2])
    cols[0].markdown("**Actif**")
    cols[1].markdown("**Montant initial ($)**")
    cols[2].markdown("**Montant actuel ($)**")

    for asset in st.session_state.assets:
        col1, col2, col3 = st.columns([2, 2, 2])
        col1.text(asset)
        initial = col2.number_input(f"Initial_{asset}", label_visibility="collapsed", min_value=0.0, value=0.0, step=100.0)
        actuel = col3.number_input(f"Actuel_{asset}", label_visibility="collapsed", min_value=0.0, value=0.0, step=100.0)
        initial_values.append(initial)
        actual_values.append(actuel)

    submitted = st.form_submit_button("Mettre à jour l'analyse")

# Analyse et affichage uniquement si données valides
if sum(initial_values) > 0 and sum(actual_values) > 0:
    df = pd.DataFrame({
        "Investissement": st.session_state.assets,
        "Initial ($)": initial_values,
        "Actuel ($)": actual_values,
    })

    df["% Initial"] = df["Initial ($)"] / df["Initial ($)"].sum() * 100
    df["% Actuel"] = df["Actuel ($)"] / df["Actuel ($)"].sum() * 100
    df["ROI (%)"] = (df["Actuel ($)"] - df["Initial ($)"]) / df["Initial ($)"] * 100

    # Tableau d'analyse
    st.subheader("📊 Résumé de l'analyse")
    st.dataframe(df.round(2), use_container_width=True)

    # Graphiques
    st.subheader("🧁 Répartition du portefeuille")

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].pie(df["% Initial"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
    axs[0].set_title("Répartition Initiale")

    axs[1].pie(df["% Actuel"], labels=df["Investissement"], autopct='%1.1f%%', startangle=90)
    axs[1].set_title("Répartition Actuelle")

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Veuillez saisir des montants valides pour afficher les résultats.")

# Footer
st.markdown("---")
st.markdown("🛠️ *Développé par 1way — ajoutez vos actifs comme REALT, staking, etc. pour suivre votre portefeuille complet.*")
