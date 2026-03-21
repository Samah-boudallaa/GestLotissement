import os
import re
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from collections import Counter

# ---- Config ----
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.secret_key = "change_this_secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["LOTS_DATA"] = []  # stockage temporaire

# ---- Fonctions utilitaires ----
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def normalize_etage(raw):
    """Nettoyer et uniformiser les valeurs d'étages"""
    s = str(raw).strip()
    if s == "" or s.lower() in ("nan", "none"):
        return ""
    s_low = s.lower()
    m = re.search(r'(\d+)', s_low)
    if m:
        return f"R+{m.group(1)}"
    return s.strip().upper()

def normalize_vocation(raw):
    """Nettoyer et uniformiser les vocations"""
    s = str(raw).strip()
    if s == "" or s.lower() in ("nan", "none"):
        return ""
    s2 = s.lower().replace("é", "e").replace("è", "e").replace("à", "a")
    if "eco" in s2 or "habitation" in s2:
        return "Economique"
    if "commercial" in s2:
        return "Commercial"
    if "villa" in s2:
        return "Villa"
    return s.strip().capitalize()

def read_lots_from_file(filepath):
    """Lire un fichier CSV/Excel et renvoyer une liste de lotissements normalisés"""
    ext = filepath.rsplit(".", 1)[1].lower()
    if ext == "csv":
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Détection souple des colonnes
    cols = {c.lower(): c for c in df.columns}
    def find_col(keys):
        for k in keys:
            for c in cols:
                if k in c:
                    return cols[c]
        return None

    col_nom = find_col(["nom", "name", "designation", "lotissement"])
    col_etages = find_col(["etage", "étage", "r+", "floor", "level"])
    col_vocation = find_col(["vocation", "usage", "type", "destin"])

    # fallback si pas trouvé
    if not col_nom or not col_etages or not col_vocation:
        use_cols = list(df.columns[:3])
        while len(use_cols) < 3:
            use_cols.append(None)
        col_nom, col_etages, col_vocation = use_cols[:3]

    lots = []
    for _, row in df.iterrows():
        nom = (str(row.get(col_nom, "")).strip() if col_nom else "").strip()
        raw_etage = row.get(col_etages, "") if col_etages else ""
        raw_vocation = row.get(col_vocation, "") if col_vocation else ""

        etage = normalize_etage(raw_etage)
        vocation = normalize_vocation(raw_vocation)

        if not nom and not etage and not vocation:
            continue

        lots.append({
            "nom": nom or "—",
            "etages": etage or "",
            "vocation": vocation or ""
        })
    return lots

# ---- Routes ----
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/import", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Aucun fichier sélectionné.", "error")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Aucun fichier sélectionné.", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            try:
                lots = read_lots_from_file(save_path)
                app.config["LOTS_DATA"] = lots
                flash(f"Fichier importé avec succès ({len(lots)} lignes lues).", "success")
                return redirect(url_for("list_lots"))
            except Exception as e:
                flash(f"Erreur lors de la lecture du fichier : {e}", "error")
                return redirect(request.url)
        else:
            flash("Format non pris en charge. Autorisé: csv, xls, xlsx.", "error")
            return redirect(request.url)
    return render_template("import.html")

@app.route("/lots")
def list_lots():
    lots = app.config.get("LOTS_DATA", [])

    # Comptage dynamique
    etages_counter = Counter([l["etages"] for l in lots if l.get("etages")])
    vocation_counter = Counter([l["vocation"] for l in lots if l.get("vocation")])

    total = len(lots)
    sum_etages = sum(etages_counter.values())
    sum_vocations = sum(vocation_counter.values())

    # Alerte si incohérence
    if sum_etages != total or sum_vocations != total:
        flash(f"⚠️ Incohérence : {sum_etages} étages et {sum_vocations} vocations détectés pour {total} lots.", "error")

    return render_template("lots.html",
                           lots=lots,
                           etages_counter=etages_counter,
                           vocation_counter=vocation_counter,
                           total=total,
                           sum_etages=sum_etages,
                           sum_vocations=sum_vocations)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route("/help")
def help_page():
    return render_template("help.html")

# ---- Lancer app ----
if __name__ == "__main__":
    app.run(debug=True, port=5000)
