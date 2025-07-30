import sys

import click

import uffutils.file
from uffutils.view import UFFDataViewer


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
@click.option("--nodes", is_flag=True)
def inspect(inputfile: str, nodes: bool):
    data = uffutils.file.read(inputfile)
    view = UFFDataViewer(data)
    if nodes:
        print(view.print_nodes())
    else:
        print(view.print_summary())


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
@click.argument("outputfile", type=click.Path())
@click.option("--node-selection", type=str, default="")
@click.option("--node-step", type=int, default=0)
@click.option("--node-count", type=int, default=0)
@click.option("--scale-length", type=float, default=1)
@click.option("--translate", type=str, default="")
def modify(
    inputfile: str,
    outputfile: str,
    node_selection: str,
    node_step: int,
    node_count: int,
    scale_length: float,
    translate: str,
):
    data = uffutils.read(inputfile)
    if node_selection or node_step or node_count:
        if node_selection:
            target_nodes = list(map(int, node_selection.split(",")))
        else:
            target_nodes = None
        data.subset(target_nodes=target_nodes, step=node_step, n_max=node_count)
    if abs(scale_length - 1) > 1e-9:
        data.scale(length=scale_length)
    if translate:
        try:
            x, y, z = [float(val) for val in translate.split(",")]
            data.translate(x, y, z)
        except Exception as e:
            sys.stderr.write(f"Couldn't parse translation '{translate}': {e}")
            sys.exit(1)
    uffutils.write(outputfile, data)
