from aiyt.utils import metadata

name = metadata["name"]
description = metadata["description"]
caption = "https://www.youtube.com/watch?v=uYZ4J7ctpio"
no_caption = "https://youtube.com/shorts/NbY29sW7gbU"
yt_demo1 = "https://youtu.be/BdSL8LLJOok"
yt_demo2 = "https://youtu.be/I5r0O7iMjKc"

readme = f"""\
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

## 📺 Demo

- {yt_demo1}
- {yt_demo2}

![screenshot](https://raw.githubusercontent.com/hoishing/aiyt/refs/heads/main/screenshots/caption.webp)

## Questions

- [Github issue]
- [LinkedIn]

[Github issue]: https://github.com/hoishing/aiyt/issues
[LinkedIn]: https://www.linkedin.com/in/kng2
"""

if __name__ == "__main__":
    with open("./README.md", "w") as f:
        f.write(readme)
