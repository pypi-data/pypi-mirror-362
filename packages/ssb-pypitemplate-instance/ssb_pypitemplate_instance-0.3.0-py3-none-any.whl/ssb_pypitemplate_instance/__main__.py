"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Pypitemplate Instance."""


if __name__ == "__main__":
    main(prog_name="ssb-pypitemplate-instance")  # pragma: no cover
