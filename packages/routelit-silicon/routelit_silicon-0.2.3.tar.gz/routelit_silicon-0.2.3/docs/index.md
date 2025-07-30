# routelit-silicon

[![Release](https://img.shields.io/github/v/release/routelit/routelit-silicon)](https://img.shields.io/github/v/release/routelit/routelit-silicon)
[![Build status](https://img.shields.io/github/actions/workflow/status/routelit/routelit-silicon/main.yml?branch=main)](https://github.com/routelit/routelit-silicon/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/routelit/routelit-silicon)](https://img.shields.io/github/commit-activity/m/routelit/routelit-silicon)
[![License](https://img.shields.io/github/license/routelit/routelit-silicon)](https://img.shields.io/github/license/routelit/routelit-silicon)

RouteLit Silicon is a Python library that extends RouteLit Builder with pre-built UI components and layouts. It provides a showcase of how to create web applications with common UI patterns like sidebars, footers, and other structural elements.

The library currently includes:

- A components builder that supports sidebar layouts
- Integration with silicon.css for styling
- Easy configuration of UI structure through a builder pattern
- Static asset management for frontend resources

## Installation

```bash
pip install routelit-silicon
```

## Usage

```python
from flask import Flask

from routelit import RouteLit
from routelit_flask import RouteLitFlaskAdapter
from routelit_silicon import RLBuilder

app = Flask(__name__)

routelit = RouteLit(BuilderClass=RLBuilder)
routelit_adapter = RouteLitFlaskAdapter(
    routelit,
    ### TO USE LOCAL VITE DEV SERVER, UNCOMMENT THE FOLLOWING LINES
    # run_mode="dev_components",
    # local_components_server="http://localhost:5173"
).configure(app)


def view(ui: RLBuilder):
    ui.set_config(use_sidebar=True)
    with ui.sidebar:
        ui.title("Sidebar")

    ui.title("Main")
    ui.text("Hello, world! from main")

    ui.sidebar.text("Hello, world! from sidebar")


@app.route("/", methods=["GET", "POST"])
def index():
    return routelit_adapter.stream_response(view)


if __name__ == "__main__":
    app.run(debug=True)
```
