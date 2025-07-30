"""Build command implementation."""

import click


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output directory for built knowledge graph",
)
def build(config: str, output: str) -> None:
    """Build knowledge representation from configured sources."""
    click.echo(f"Building using config from {config} to {output}")


def build_knowledge() -> None:
    """Build knowledge representation from configured sources."""
    # Implementation details will go here
