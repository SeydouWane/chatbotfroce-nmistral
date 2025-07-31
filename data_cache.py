import os
import json
from datetime import datetime, timedelta
from utils import get_text_from_url

CACHE_FILE = "force_content.json"
EXPIRATION_DAYS = 90  

URLS = [
    "https://preprod2.force-n.sn/a-propos",
    #"https://urlz.fr/lB3G",
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

def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    modified_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return datetime.now() - modified_time < timedelta(days=EXPIRATION_DAYS)

def load_cached_content():
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("content", "")

def save_content_to_cache(content):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"content": content}, f)

def get_force_content():
    if is_cache_valid():
        print(" Chargement du contenu FORCE-N depuis le cache local.")
        return load_cached_content()

    print("Scraping du site FORCE-N...")
    all_texts = [get_text_from_url(url) for url in URLS]
    full_text = "\n\n".join(all_texts)[:10000]

    save_content_to_cache(full_text)
    print(" Contenu sauvegardé dans le cache.")
    return full_text
