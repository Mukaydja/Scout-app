import streamlit as st
from datetime import date
from fpdf import FPDF

st.set_page_config(page_title="Scouting Rapports", layout="centered")

# Sidebar
version = st.sidebar.radio("Choisir la version", options=["PC", "Mobile"])
st.title("📝 Rapport de Scouting Football")

# Infos joueur & observation
with st.expander("Infos joueur & observation", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        age = st.number_input("Âge", min_value=5, max_value=60, step=1)
        categorie = st.selectbox("Catégorie", ["U12", "U13", "U14", "U15", "U16", "U17", "U18", "U19", "Senior"])
        club = st.text_input("Club")
    with col2:
        date_obs = st.date_input("Date de l'observation", value=date.today())
        observateur = st.text_input("Nom de l'observateur")
        nb_fois = st.number_input("Nombre de fois observé", min_value=1, max_value=50, step=1)
        adversaire = st.text_input("Adversaire")
        lieu = st.selectbox("Lieu", ["Domicile", "Extérieur"])
        competition = st.text_input("Compétition")

# Poste observé
poste = st.selectbox("Poste observé", options=["Gardien", "Défenseur", "Milieu", "Attaquant"], index=1)

criteres_par_poste = {
    "Gardien": {
        "Offensif": ["Lancements longs", "Relances", "Jeu au pied"],
        "Défensif": ["Arrêts", "Sorties aériennes", "Anticipation", "Communication", "Positionnement"]
    },
    "Défenseur": {
        "Offensif": ["Montées", "Passes clés", "Centres", "Jeu au pied"],
        "Défensif": ["Tacles", "Interceptions", "Marquage", "Duels aériens", "Positionnement"]
    },
    "Milieu": {
        "Offensif": ["Passes décisives", "Progressions balle au pied", "Création d'espaces", "Tirs"],
        "Défensif": ["Pressing", "Récupérations", "Marquage", "Repli défensif"]
    },
    "Attaquant": {
        "Offensif": ["Finition", "Dribbles", "Appels", "Jeu dos au but"],
        "Défensif": ["Pressing haut", "Repli", "Conservation balle"]
    }
}

criteres_off = criteres_par_poste[poste]["Offensif"]
criteres_def = criteres_par_poste[poste]["Défensif"]

# Notes & Commentaires
st.header(f"📝 Critères Offensifs et Défensifs pour {poste}")

if version == "PC":
    cols_off = st.columns(2)
    container_off = cols_off[0]
    container_def = cols_off[1]
else:
    container_off = st.container()
    container_def = st.container()

notes_off = {}
comms_off = {}
notes_def = {}
comms_def = {}

with container_off:
    st.subheader("Offensif")
    for i, crit in enumerate(criteres_off):
        crit_mod = st.text_input(f"Critère Offensif #{i+1}", value=crit, key=f"off_crit_{i}")
        notes_off[crit_mod] = st.slider(f"Note - {crit_mod}", 0, 10, 5, key=f"off_note_{i}")
        comms_off[crit_mod] = st.text_area(f"Commentaire - {crit_mod}", height=80, key=f"off_comm_{i}")

with container_def:
    st.subheader("Défensif")
    for i, crit in enumerate(criteres_def):
        crit_mod = st.text_input(f"Critère Défensif #{i+1}", value=crit, key=f"def_crit_{i}")
        notes_def[crit_mod] = st.slider(f"Note - {crit_mod}", 0, 10, 5, key=f"def_note_{i}")
        comms_def[crit_mod] = st.text_area(f"Commentaire - {crit_mod}", height=80, key=f"def_comm_{i}")

commentaire_general = st.text_area("Commentaire général", height=100)

def create_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 60, 90)
    pdf.cell(0, 15, "Rapport de Scouting Football", ln=True, align="C")
    pdf.ln(4)

    # --- Informations générales ---
    pdf.set_fill_color(230, 240, 250)
    pdf.set_draw_color(30, 60, 90)
    pdf.set_line_width(0.7)
    y_info = pdf.get_y()
    pdf.rect(10, y_info, 190, 60, style="DF")
    pdf.set_xy(15, y_info + 3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Informations générales", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)

    infos = [
        f"Nom complet : {prenom} {nom}",
        f"Âge : {age} ans",
        f"Catégorie : {categorie}",
        f"Club : {club}",
        f"Date observation : {date_obs.strftime('%d/%m/%Y')}",
        f"Observateur : {observateur}",
        f"Nombre fois observé : {nb_fois}",
        f"Adversaire : {adversaire}",
        f"Lieu : {lieu}",
        f"Compétition : {competition}",
        f"Poste observé : {poste}"
    ]

    for info in infos:
        pdf.set_x(15)
        pdf.cell(0, 7, info, ln=True)

    pdf.ln(8)

    # -----------------------------
    # CRITÈRES OFFENSIFS
    # -----------------------------
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(10, 40, 80)
    pdf.cell(0, 10, "Critères Offensifs", border=1, fill=True, ln=True, align="C")

    col_widths = [50, 20, 120]
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(col_widths[0], 8, "Critère", border=1)
    pdf.cell(col_widths[1], 8, "Note", border=1, align="C")
    pdf.cell(col_widths[2], 8, "Commentaire", border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 11)
    for crit in notes_off:
        note = notes_off[crit]
        comm = comms_off.get(crit, "")
        y_start = pdf.get_y()
        x_start = pdf.get_x()
        comment_lines = pdf.multi_cell(col_widths[2], 6, comm, border=0, split_only=True)
        crit_lines = pdf.multi_cell(col_widths[0], 6, crit, border=0, split_only=True)
        max_lines = max(len(comment_lines), len(crit_lines), 1)
        row_height = max_lines * 6
        pdf.set_xy(x_start, y_start)
        pdf.multi_cell(col_widths[0], 6, crit, border=1)
        final_y_crit = pdf.get_y()
        pdf.set_xy(x_start + col_widths[0], y_start)
        pdf.multi_cell(col_widths[1], row_height, str(note), border=1, align="C")
        pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)
        pdf.multi_cell(col_widths[2], 6, comm, border=1)
        pdf.set_y(max(final_y_crit, y_start + row_height))

    pdf.ln(5)

    # -----------------------------
    # CRITÈRES DÉFENSIFS
    # -----------------------------
    pdf.set_fill_color(255, 220, 220)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(80, 10, 10)
    pdf.cell(0, 10, "Critères Défensifs", border=1, fill=True, ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(col_widths[0], 8, "Critère", border=1)
    pdf.cell(col_widths[1], 8, "Note", border=1, align="C")
    pdf.cell(col_widths[2], 8, "Commentaire", border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 11)
    for crit in notes_def:
        note = notes_def[crit]
        comm = comms_def.get(crit, "")
        y_start = pdf.get_y()
        x_start = pdf.get_x()
        comment_lines = pdf.multi_cell(col_widths[2], 6, comm, border=0, split_only=True)
        crit_lines = pdf.multi_cell(col_widths[0], 6, crit, border=0, split_only=True)
        max_lines = max(len(comment_lines), len(crit_lines), 1)
        row_height = max_lines * 6
        pdf.set_xy(x_start, y_start)
        pdf.multi_cell(col_widths[0], 6, crit, border=1)
        final_y_crit = pdf.get_y()
        pdf.set_xy(x_start + col_widths[0], y_start)
        pdf.multi_cell(col_widths[1], row_height, str(note), border=1, align="C")
        pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)
        pdf.multi_cell(col_widths[2], 6, comm, border=1)
        pdf.set_y(max(final_y_crit, y_start + row_height))

    pdf.ln(10)

    # --- Commentaire général et note moyenne ---
    toutes_notes = list(notes_off.values()) + list(notes_def.values())
    moyenne = round(sum(toutes_notes) / len(toutes_notes), 2) if toutes_notes else 0
    texte_commentaire = commentaire_general.strip() or "-"
    texte_affiche = f"Commentaire général : {texte_commentaire}"
    largeur_commentaire = 190 - 2 * 10
    pdf.set_font("Helvetica", "", 11)
    lignes = pdf.multi_cell(largeur_commentaire, 7, texte_affiche, border=0, align='L', split_only=True)
    hauteur_ligne = 7
    hauteur_totale = hauteur_ligne * len(lignes) + 15
    y_start = pdf.get_y()
    pdf.set_fill_color(240, 240, 240)
    pdf.set_draw_color(30, 60, 90)
    pdf.set_line_width(0.7)
    pdf.rect(10, y_start, 190, hauteur_totale, style="DF")
    pdf.set_xy(15, y_start + 5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 60, 90)
    pdf.cell(0, 8, f"Note moyenne : {moyenne} / 10", ln=True)
    pdf.set_xy(15, y_start + 15)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    for ligne in lignes:
        pdf.cell(0, hauteur_ligne, ligne, ln=True)

    # ✅ Fix final ici (important)
    return pdf.output(dest="S").encode("latin1", errors="ignore")

if st.button("Générer le PDF"):
    pdf_bytes = create_pdf()
    st.success("✅ PDF généré avec succès !")
    st.download_button(label="📥 Télécharger le PDF", data=pdf_bytes, file_name=f"rapport_{prenom}_{nom}.pdf", mime="application/pdf")
