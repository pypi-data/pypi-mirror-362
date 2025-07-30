"""Command-line interface for babbl."""

import traceback
from pathlib import Path
from typing import Optional

import click

from babbl.load import load_file, load_metadata, save_file
from babbl.parser import BabblParser
from babbl.renderer import HTMLRenderer


@click.group()
@click.version_option()
def main():
    """Babbl: Turn markdown into beautiful research blog posts."""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output HTML file path"
)
@click.option("--css", type=click.Path(path_type=Path), help="Path to CSS file")
@click.option("--toc", is_flag=True, help="Generate table of contents for h1 headings")
@click.option(
    "--base-path",
    type=click.Path(path_type=Path),
    help="Base path for resolving code references",
)
def render(
    input_file: Path,
    output: Optional[Path],
    css: Optional[Path],
    toc: bool,
    base_path: Optional[Path],
):
    """Render a markdown file to HTML."""
    if output is None:
        output_path = input_file.with_suffix(".html")
    else:
        output_path = output

    parser = BabblParser()
    renderer = HTMLRenderer(
        css_file_path=css,
        show_toc=toc,
        base_path=base_path,
        current_file_path=input_file,
    )

    try:
        contents = load_file(input_file)
        metadata, contents = load_metadata(contents)
        document = parser.parse(contents)
        html = renderer.html(document, metadata)
        save_file(output_path, html)
        click.echo(f"Successfully rendered: {output_path}")
    except Exception as e:
        click.echo(f"Error rendering file: {e}", err=True)
        click.echo(f"Full traceback:\n{traceback.format_exc()}", err=True)
        raise click.Abort()


@main.command()
@click.argument(
    "input_dir", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option(
    "--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory"
)
@click.option("--pattern", default="*.md", help="File pattern to match")
@click.option(
    "--recursive", "-r", is_flag=True, help="Process subdirectories recursively"
)
@click.option("--css", type=click.Path(path_type=Path), help="Path to CSS file")
@click.option("--toc", is_flag=True, help="Generate table of contents for h1 headings")
@click.option(
    "--base-path",
    type=click.Path(path_type=Path),
    help="Base path for resolving code references",
)
def build(
    input_dir: Path,
    output_dir: Optional[Path],
    pattern: str,
    recursive: bool,
    css: Optional[Path],
    toc: bool,
    base_path: Optional[Path],
):
    """Build multiple markdown files in a directory."""
    if output_dir is None:
        output_dir = input_dir / "output"
    output_dir.mkdir(exist_ok=True)

    if recursive:
        md_files = list(input_dir.rglob(pattern))
    else:
        md_files = list(input_dir.glob(pattern))

    if not md_files:
        click.echo(f"No markdown files found matching pattern '{pattern}'")
        return

    click.echo(f"Found {len(md_files)} markdown files to process...")

    parser = BabblParser()

    for md_file in md_files:
        try:
            # Create a renderer for each file to pass the current file path
            renderer = HTMLRenderer(
                css_file_path=css,
                show_toc=toc,
                base_path=base_path,
                current_file_path=md_file,
            )

            rel_path = md_file.relative_to(input_dir)
            output_file = output_dir / rel_path.with_suffix(".html")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            contents = load_file(md_file)
            metadata, contents = load_metadata(contents)
            document = parser.parse(contents)
            html = renderer.html(document, metadata)
            save_file(output_file, html)
            click.echo(f"✓ {md_file.name} → {output_file}")

        except Exception as e:
            click.echo(f"✗ Error processing {md_file.name}: {e}", err=True)
            click.echo(f"Full traceback:\n{traceback.format_exc()}", err=True)

    click.echo(f"\nBuild complete! Output directory: {output_dir}")
