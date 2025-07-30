import tomlkit
from aiyt import metadata
from textwrap import dedent


def update_readme():
    name = metadata["name"]
    description = metadata["description"]
    # caption = "https://www.youtube.com/watch?v=uYZ4J7ctpio"
    # no_caption = "https://youtube.com/shorts/NbY29sW7gbU"

    readme = dedent(f"""\
        # {name}

        > {description}

        ## Usage

        - run with `uvx`

        ```bash
        uvx {name}
        ```

        - install locally

        ```bash
        uv tool install {name}

        # then run it
        {name}
        ```

        - upgrade to the lastest version

        ```bash
        uvx {name}@latest

        # upgrade installed tool
        uv tool upgrade {name}@latest
        ```

        ## Questions

        - [Github issue]
        - [LinkedIn]

        [Github issue]: https://github.com/hoishing/aiyt/issues
        [LinkedIn]: https://www.linkedin.com/in/kng2
        """)
    with open("./README.md", "w") as f:
        f.write(readme)


def update_pyproject():
    with open("pyproject.toml", "r") as f:
        data = tomlkit.load(f)
    for key in ["name", "version", "description"]:
        data["project"][key] = metadata[key]
    with open("pyproject.toml", "w") as f:
        tomlkit.dump(data, f)


if __name__ == "__main__":
    update_readme()
    update_pyproject()
