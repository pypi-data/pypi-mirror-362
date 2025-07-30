"""CLI for tap-canvas-temple."""

from tap_canvas_temple.tap import TapCanvas

def cli():
    """Run the tap CLI."""
    TapCanvas.cli()

if __name__ == "__main__":
    cli()