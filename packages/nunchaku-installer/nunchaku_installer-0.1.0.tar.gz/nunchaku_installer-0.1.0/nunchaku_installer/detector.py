# nunchaku_installer/detector.py
import sys
import platform
import importlib.metadata
from typing import Optional, Dict

def get_system_info() -> Dict[str, str]:
    """
    Détecte l'OS, l'architecture et la version de Python.
    Retourne un dictionnaire avec 'os', 'python_version', 'torch_version'.
    """
    os_name = platform.system().lower()
    if os_name == "linux":
        os_key = "linux"
    elif os_name == "windows":
        os_key = "win"
    else:
        # Note : On lève directement l'exception intégrée ici
        raise NotImplementedError(f"Le système d'exploitation '{os_name}' n'est pas supporté.")

    py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    torch_version = get_torch_version_string()

    return {
        "os": os_key,
        "python_version": py_version,
        "torch_version": torch_version,
    }

def get_torch_version_string() -> Optional[str]:
    """
    Tente de trouver la version de PyTorch SANS l'importer, en lisant les métadonnées.
    Retourne None si PyTorch n'est pas installé ou si la version est invalide.
    """
    try:
        version = importlib.metadata.version("torch")
        
        # AJOUT DE LA VÉRIFICATION DÉFENSIVE
        if not version:
            return None

        version_parts = version.split('.')
        torch_str = f"torch{version_parts[0]}.{version_parts[1]}"
        return torch_str
    except importlib.metadata.PackageNotFoundError:
        return None