import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from bs4 import BeautifulSoup
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# CONFIGURATION
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("⚠️ La variable d’environnement HF_TOKEN n’est pas définie.")

client = InferenceClient(token=HF_TOKEN)

# FLASK APP
app = Flask(__name__)
CORS(app)

# Formulaire d'inscription
INSCRIPTION_URL = "https://forcen.jotform.com/form/231154488427359"

# URLS À SCRAPER
URLS = [
    "https://preprod2.force-n.sn/a-propos",
    "https://preprod2.force-n.sn/les-composantes",
    "https://preprod2.force-n.sn/qui-sommes-nous",
    "https://preprod2.force-n.sn/missions-et-objectfis",
    "https://preprod2.force-n.sn/les-partenaires",
    "https://preprod2.force-n.sn/faq",
    "https://preprod2.force-n.sn/formations",
    "https://preprod2.force-n.sn/formations/e-business",
    "https://preprod2.force-n.sn/formations/intelligence-artificielle-et-data",
    "https://preprod2.force-n.sn/formations/developpement-logiciel",
    "https://preprod2.force-n.sn/formations/technologies-emergentes-et-cybersecurite",
    "https://preprod2.force-n.sn/sigui",
    "https://preprod2.force-n.sn/parcours-initiatique",
    "https://preprod2.force-n.sn/parcours-daccompagnement",
    "https://preprod2.force-n.sn/opportunites",
    "https://preprod2.force-n.sn/opportunites/vous-etes-entreprise",
    "https://preprod2.force-n.sn/opportunites/vous-etes-entrepreneur",
    "https://preprod2.force-n.sn/promotion-des-sciences",
    "https://preprod2.force-n.sn/actualites",
    "https://preprod2.force-n.sn/jpo-2024",
    "https://preprod2.force-n.sn/services/formations",
    "https://preprod2.force-n.sn/services/accompagnement-linsertion-professionnelle",
    "https://preprod2.force-n.sn/services/promotion-des-sciences",
    "https://preprod2.force-n.sn/certificat/commerce-digital",
    "https://preprod2.force-n.sn/certificat/cybersecurite",
    "https://preprod2.force-n.sn/certificat/data-analysis",
    "https://preprod2.force-n.sn/certificat/data-engineering",
    "https://preprod2.force-n.sn/certificat/developpement-logiciel-java",
    "https://preprod2.force-n.sn/certificat/developpement-logiciel-php",
    "https://preprod2.force-n.sn/certificat/developpement-logiciel-python",
    "https://preprod2.force-n.sn/certificat/developpement-mobile",
    "https://preprod2.force-n.sn/certificat/ecriture-de-scenario",
    "https://preprod2.force-n.sn/certificat/entrepreneuriat-numerique",
    "https://preprod2.force-n.sn/certificat/front-end",
    "https://preprod2.force-n.sn/certificat/intelligence-artificielle-pour-tous",
    "https://preprod2.force-n.sn/certificat/intelligence-artificielle-traitement-du-langage-naturel-vision-par-ordinateur",
    "https://preprod2.force-n.sn/certificat/marketing-digital",
    "https://preprod2.force-n.sn/certificat/no-code-low-code",
    "https://preprod2.force-n.sn/certificat/traitement-de-donnees-niveaux-1-2",
    "https://preprod2.force-n.sn/certificat/web-3",
]

# Cache mémoire simple
force_content_cache = None

# SCRAPING + CACHING
def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"[Erreur] {url} — {e}")
        return ""

def get_force_content():
    global force_content_cache
    if force_content_cache:
        print("✅ Chargement depuis le cache mémoire.")
        return force_content_cache

    print("🔄 Scraping des pages FORCE-N...")
    all_texts = [get_text_from_url(url) for url in URLS]
    full_text = "\n\n".join(all_texts)[:10000]

    force_content_cache = full_text
    print("✅ Contenu stocké en cache mémoire.")
    return full_text

full_text = get_force_content()

# CHATBOT LOGIC
def ask_force_n_bot(message, context_text):
    system_prompt = (
        "Tu es AWA, la voix officielle du programme FORCE-N. "
        "Sois institutionnelle, claire, sans inventer."
        "Réponds uniquement à partir des informations suivantes :\n\n"
        f"{context_text}\n\n"
        "Si l’information n’est pas présente, dis : "
        "'Je suis désolée, je n’ai pas cette information.'"
    )

    if "inscription" in message.lower() or "s'inscrire" in message.lower():
        return (
            "Pour t'inscrire aux formations de FORCE-N, merci de remplir ce formulaire officiel :\n"
            f"{INSCRIPTION_URL}\n\n"
            "Tu y trouveras toutes les informations nécessaires à ta pré-candidature."
        )

    completion = client.chat_completion(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        max_tokens=400,
        temperature=0.7
    )
    return completion.choices[0].message["content"]

# ROUTES FLASK
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message manquant"}), 400

    bot_response = ask_force_n_bot(user_message, full_text)
    return jsonify({"response": bot_response})

@app.route("/")
def home():
    return send_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)

# Pour Render
application = app
