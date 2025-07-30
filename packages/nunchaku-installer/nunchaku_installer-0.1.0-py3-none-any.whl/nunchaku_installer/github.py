# nunchaku_installer/github.py
import json
import urllib.request
from typing import List, Dict

API_URL = "https://api.github.com/repos/nunchaku-tech/nunchaku"

def _get_json_from_url(url: str) -> Dict | List[Dict]:
    """
    Fonction helper pour faire une requête GET et parser la réponse JSON.
    """
    try:
        # Il est important de définir un User-Agent, sinon GitHub peut bloquer la requête.
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'nunchaku-installer'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise urllib.error.URLError(f"GitHub API returned status {response.status}")
            data = response.read()
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"Erreur réseau ou HTTP lors de la connexion à l'API GitHub : {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage de la réponse JSON de GitHub : {e}")
        raise


def get_releases() -> List[Dict]:
    """Récupère toutes les releases depuis l'API GitHub."""
    return _get_json_from_url(f"{API_URL}/releases")

def get_latest_release() -> Dict:
    """Récupère la dernière release."""
    return _get_json_from_url(f"{API_URL}/releases/latest")

def get_release_by_tag(tag: str) -> Dict:
    """Récupère une release spécifique par son tag."""
    return _get_json_from_url(f"{API_URL}/releases/tags/{tag}")