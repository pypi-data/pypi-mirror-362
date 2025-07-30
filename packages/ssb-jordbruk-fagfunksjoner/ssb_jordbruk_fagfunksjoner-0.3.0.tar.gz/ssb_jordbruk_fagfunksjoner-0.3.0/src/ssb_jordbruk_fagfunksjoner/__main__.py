"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Jordbruk Fagfunksjoner."""


if __name__ == "__main__":
    main(prog_name="ssb-jordbruk-fagfunksjoner")  # pragma: no cover
