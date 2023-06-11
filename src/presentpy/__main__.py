from pathlib import Path

import click


@click.command()
@click.argument('notebook', type=click.Path(exists=True))
def run_presentpy(notebook):
    notebook_path = Path(notebook)

    print(f'Running {notebook_path}...')

if __name__ == '__main__':
    run_presentpy()
