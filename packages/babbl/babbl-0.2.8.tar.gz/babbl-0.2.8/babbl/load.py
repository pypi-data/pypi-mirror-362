"""Miscellaneous utilities."""

from pathlib import Path

import yaml


def load_file(path: Path) -> str:
    """Get the contents of a file as a string."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_file(path: Path, contents: str) -> None:
    """Save contents to an HTML file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)


def load_metadata(contents: str) -> tuple[dict[str, str], str]:
    """Parse the frontmatter of a markdown file.

    This function robustly detects and parses YAML frontmatter that is delimited
    by `---` at the beginning and end of the document.

    Args:
        contents: The raw markdown content

    Returns:
        A tuple of (metadata_dict, content_without_frontmatter)
    """
    lines = contents.split("\n")

    # check if the file starts with frontmatter delimiter
    if not lines or not lines[0].strip() == "---":
        return {}, contents

    # find the closing ---
    frontmatter_lines = []
    content_lines = []
    in_frontmatter = True

    for i, line in enumerate(lines[1:], 1):  # start from second line
        if in_frontmatter:
            if line.strip() == "---":
                # found closing delimiter
                in_frontmatter = False
                content_lines = lines[i + 1 :]  # Everything after the closing ---
                break
            else:
                frontmatter_lines.append(line)
        else:
            content_lines.append(line)

    # if we didn't find a closing ---, there's no valid frontmatter
    if in_frontmatter:
        return {}, contents

    # parse the frontmatter
    try:
        frontmatter_text = "\n".join(frontmatter_lines)
        metadata = yaml.safe_load(frontmatter_text) or {}
        content = "\n".join(content_lines)
        return metadata, content
    except yaml.YAMLError:
        # if YAML parsing fails, treat as regular content
        return {}, contents
