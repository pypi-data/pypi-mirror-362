import click
from subprocess import Popen


@click.command()
@click.version_option()
def main():
    """Launch the Streamlit app."""

    cmd = "uv run streamlit run aiyt/main.py"
    process = Popen(cmd.split())
    process.wait()


if __name__ == "__main__":
    main()
