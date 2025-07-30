# nunchaku_installer/cli.py
import typer
from typing_extensions import Annotated

from . import detector, github, logic

app = typer.Typer(help="Un installateur simple pour la librairie Nunchaku.")

@app.command()
def install(
    version: Annotated[str, typer.Option("--version", "-v", help="La version de Nunchaku à installer (ex: v0.3.1). 'latest' par défaut.")] = "latest",
    backend: Annotated[str, typer.Option("--backend", "-b", help="Le gestionnaire de paquet à utiliser ('pip' ou 'uv').")] = "pip",
):
    """
    Détecte votre configuration et installe la version compatible de Nunchaku.
    """
    typer.echo("Bienvenue dans l'installateur Nunchaku !")
    
    try:
        typer.echo("🔍 Détection de la configuration système...")
        sys_info = detector.get_system_info()
        typer.echo(f"   - OS: {sys_info['os']}")
        typer.echo(f"   - Python: {sys_info['python_version']}")
        if sys_info['torch_version']:
            typer.echo(f"   - PyTorch détecté: {sys_info['torch_version']}")
        else:
            typer.echo("   - PyTorch: non détecté")
        
        typer.echo(f"\n⬇️ Recherche de la release Nunchaku '{version}' sur GitHub...")
        if version == "latest":
            release_data = github.get_latest_release()
        else:
            release_data = github.get_release_by_tag(version)
        
        typer.echo(f"Found release: {release_data['name']}")

        assets = release_data.get("assets", [])
        wheel_to_install = logic.find_compatible_wheel(assets, sys_info)

        if not wheel_to_install:
            typer.secho("\n❌ Impossible de trouver un wheel compatible pour votre configuration.", fg=typer.colors.RED)
            typer.echo("   - OS Requis: linux ou windows")
            typer.echo("   - Python Requis: 3.10, 3.11, ou 3.12")
            typer.echo("Vérifiez les assets disponibles sur la page de la release GitHub.")
            raise typer.Exit(1)

        typer.secho(f"\n🎯 Wheel compatible trouvé : {wheel_to_install['name']}", fg=typer.colors.GREEN)

        logic.install_wheel(wheel_to_install['url'], backend.lower())

    # CORRECTION DE L'EXCEPTION ICI
    except NotImplementedError as e:
        typer.secho(f"Erreur: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"\nUne erreur inattendue est survenue: {e}", fg=typer.colors.RED)
        typer.echo("Vérifiez votre connexion internet et que le tag de la release existe bien.")
        raise typer.Exit(1)


@app.command(name="list-versions")
def list_versions():
    """
    Liste toutes les versions de Nunchaku disponibles sur GitHub.
    """
    typer.echo("🔍 Recherche des versions disponibles de Nunchaku...")
    try:
        releases = github.get_releases()
        if not releases:
            typer.echo("Aucune version trouvée.")
            return
        
        typer.echo("Versions disponibles :")
        for release in releases:
            typer.echo(f" - {release['tag_name']} ({release['name']})")
            
    except Exception as e:
        typer.secho(f"Erreur lors de la récupération des versions : {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()