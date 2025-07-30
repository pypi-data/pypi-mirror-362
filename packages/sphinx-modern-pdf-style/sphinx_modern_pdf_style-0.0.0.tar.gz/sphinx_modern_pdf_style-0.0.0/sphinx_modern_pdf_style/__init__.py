"""Sphinx configuration for Latex PDF using Xetex"""
from typing import Any
from sphinx.application import Sphinx
from pathlib import Path
import shutil

__version__ = "0.1.0"

assets_dir = Path(__file__).parent / "assets"

def copy_custom_files(app: Sphinx) -> None:
    """Copy image files to project for use in PDF generation"""
    if app.builder.format == "latex":
        shutil.copytree(str(assets_dir), app.outdir, dirs_exist_ok=True)

def setup(app: Sphinx) -> dict[str, Any]:
    """Configure the main extension and theme."""
    app.setup_extension("sphinx_modern_pdf_style.config")
    app.connect(  # pyright: ignore [reportUnknownMemberType]
        "builder-inited",
        copy_custom_files,
    )
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

__all__ = ["__version__", "setup"]