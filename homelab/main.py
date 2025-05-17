from pathlib import Path
from typing import Annotated, List

import typer
import yaml
import os

app = typer.Typer()


def get_containers(path: Path) -> List[str]:
    with open((path / "containers_list.yml"), 'r') as file:
        yml = yaml.safe_load(file)
        return [str(Path(f"{container}")) for container in yml['containers']]


@app.command()
def test(containers_path: Annotated [Path, typer.Argument()] = Path('.')):
    for container in get_containers(containers_path):
        os.system(f'ls {container}')

@app.command()
def plop():
    print("lop")
#
@app.command()
def stop(containers_path: Annotated [Path, typer.Argument()] = Path('.')):
    """
    Stop all containers in the list.
    :param containers_path:
    :return:
    """
    for container in get_containers(containers_path):
        os.system(f"docker compose down {container}")

@app.command()
def start(containers_path: Annotated [Path, typer.Argument()] = Path('.'), detach: bool = True, force_recreate: bool = False):
    """
    Start all containers in the list.
    :param containers_path:
    :param detach:
    :param force_recreate:
    :return:
    """
    for container in get_containers(containers_path):
        os.system(f"docker compose up {'-d' if detach else ''} {'--force-recreate' if force_recreate else ''} {container}")

@app.command()
def pull(containers_path: Annotated [Path, typer.Argument()] = Path('.')):
    """
    Pull all containers in the list.
    :param containers_path:
    :return:
    """
    for container in get_containers(containers_path):
        os.system(f"docker compose pull {container}")

if __name__ == "__main__":
    app()