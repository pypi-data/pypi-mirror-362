# cli.py
import sys
import json
import argparse
from cacao import App
from cacao_json_viewer.viewer import JSONViewerPage

def main():
    parser = argparse.ArgumentParser(
        prog="cacao-json-viewer",
        description="Open a desktop JSON/tree viewer using Cacao"
    )
    parser.add_argument(
        "json_file", nargs="?", type=argparse.FileType("r"),
        default=sys.stdin,
        help="Path to JSON file (or omit to read from STDIN)"
    )
    args = parser.parse_args()

    # Load JSON
    try:
        data = json.load(args.json_file)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Create app and set up the page
    app = App()
    viewer = JSONViewerPage(data)
    @app.mix("/")
    def home():
        return viewer.render()

    # Brew as desktop window
    app.brew(
        type="desktop",
        title="Cacao JSON Viewer",
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
    )

if __name__ == "__main__":
    main()