# nunchaku_installer/logic.py
import re
import subprocess
import sys
from typing import List, Dict, Optional
from packaging.version import parse as parse_version

def find_compatible_wheel(assets: List[Dict], sys_info: Dict[str, str]) -> Optional[Dict]:
    """
    Trouve le meilleur .whl compatible dans la liste des assets d'une release.
    """
    compatible_wheels = []
    
    wheel_regex = re.compile(
        r"nunchaku-.+\+(torch[\d.]+)-(cp\d+)-.+-(linux_x86_64|win_amd64)\.whl"
    )

    for asset in assets:
        match = wheel_regex.match(asset['name'])
        if match:
            torch_v, python_v, os_v_arch = match.groups()
            os_key = "linux" if "linux" in os_v_arch else "win"

            if sys_info["os"] == os_key and sys_info["python_version"] == python_v:
                asset_info = {
                    "url": asset["browser_download_url"],
                    "name": asset["name"],
                    "torch_version_str": torch_v,
                    "torch_version_obj": parse_version(torch_v.replace("torch", ""))
                }
                compatible_wheels.append(asset_info)

    if not compatible_wheels:
        return None

    if sys_info["torch_version"]:
        for wheel in compatible_wheels:
            if wheel["torch_version_str"] == sys_info["torch_version"]:
                print(f"✅ Trouvé : wheel compatible avec votre version de PyTorch ({sys_info['torch_version']}).")
                return wheel
        print(f"⚠️ Aucun wheel ne correspond exactement à votre version de PyTorch ({sys_info['torch_version']}).")

    print("✨ Sélection du wheel avec la version de PyTorch la plus récente.")
    best_wheel = max(compatible_wheels, key=lambda w: w["torch_version_obj"])
    return best_wheel


def install_wheel(wheel_url: str, backend: str):
    """
    Installe un .whl depuis une URL en utilisant 'pip' ou 'uv'.
    Cette version laisse le sous-processus écrire directement dans le terminal.
    """
    if backend not in ["pip", "uv"]:
        raise ValueError("Le backend doit être 'pip' ou 'uv'.")

    print(f"\n🚀 Lancement de l'installation avec '{backend}'...")
    print(f"URL du wheel : {wheel_url}")

    try:
        # On construit la commande de base
        command = [sys.executable, "-m", backend, "pip", "install", wheel_url, "--force-reinstall"]
        
        # Pour uv, on peut lui dire explicitement de garder les couleurs s'il ne le fait pas automatiquement.
        # Mais en ne capturant pas la sortie, il devrait le faire tout seul.
        if backend == "uv":
             # La commande pour 'uv' est légèrement différente: `uv pip install`
             command = [sys.executable, "-m", "uv", "pip", "install", wheel_url, "--force-reinstall"]
        else: # pip
             command = [sys.executable, "-m", "pip", "install", wheel_url, "--force-reinstall"]

        # On exécute la commande et on attend qu'elle se termine.
        # En ne spécifiant pas `stdout` ou `stderr`, ils sont hérités du parent,
        # ce qui signifie que la sortie (avec couleurs et animations) ira directement au terminal.
        result = subprocess.run(command, check=False) # check=False pour gérer l'erreur nous-mêmes

        if result.returncode == 0:
            print("\n✅ Installation de Nunchaku terminée avec succès !")
        else:
            print(f"\n❌ Erreur lors de l'installation (code de sortie: {result.returncode}).")
            print("Veuillez vérifier les messages d'erreur ci-dessus.")

    except FileNotFoundError:
        print(f"❌ Erreur : La commande '{backend}' n'a pas été trouvée.")
        print(f"Assurez-vous que '{backend}' est installé et dans votre PATH.")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")