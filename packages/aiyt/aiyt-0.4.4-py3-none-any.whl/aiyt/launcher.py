import click
from pathlib import Path
from subprocess import Popen


@click.command()
@click.version_option()
def main():
    """Launch the Streamlit app."""

    cmd = f"uv run streamlit run {Path(__file__).parent / 'main.py'}"
    process = Popen(cmd.split())
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        exit(0)


if __name__ == "__main__":
    main()
