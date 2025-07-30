"""Miscellaneous utilities."""

import ast
import glob
import re
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


# Code reference functions (moved from code_ref.py)
from typing import List, Optional


def resolve_path(file_path: str, base_path: Optional[Path] = None, current_file_path: Optional[Path] = None) -> Path:
    path = Path(file_path)
    if path.is_absolute():
        return path
    if current_file_path:
        relative_path = (current_file_path.parent / path).resolve()
        if relative_path.exists():
            return relative_path
    base = base_path or Path.cwd()
    return (base / path).resolve()


def extract_code(
    file_path: str,
    reference: str,
    syntax_type: str = "link",
    base_path: Optional[Path] = None,
    current_file_path: Optional[Path] = None,
) -> Optional[str]:
    try:
        if syntax_type == "hash" and not file_path:
            return extract_hash_reference(reference, base_path)
        full_path = resolve_path(file_path, base_path, current_file_path)
        if not full_path.exists():
            return None
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        if file_path.lower().endswith(".html"):
            return extract_html_content(content, reference)
        lines = content.split("\n")
        code = extract_by_function_class(lines, reference)
        if code:
            return code
        code = extract_by_line_numbers(lines, reference)
        if code:
            return code
        code = extract_by_line_range(lines, reference)
        if code:
            return code
        return None
    except Exception:
        return None


def extract_by_function_class(lines: List[str], reference: str) -> Optional[str]:
    try:
        content = "\n".join(lines)
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name == reference:
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line + 1
                    end_line = find_block_end(lines, start_line, node)
                    return "\n".join(lines[start_line:end_line])
        return None
    except Exception:
        return None


def extract_by_line_numbers(lines: List[str], reference: str) -> Optional[str]:
    line_match = re.match(r"line\s+(\d+)", reference, re.IGNORECASE)
    if line_match:
        line_num = int(line_match.group(1)) - 1
        if 0 <= line_num < len(lines):
            return lines[line_num]
    return None


def extract_by_line_range(lines: List[str], reference: str) -> Optional[str]:
    range_match = re.match(r"lines?\s+(\d+)[-:]\s*(\d+)", reference, re.IGNORECASE)
    if range_match:
        start_line = int(range_match.group(1)) - 1
        end_line = int(range_match.group(2))
        if 0 <= start_line < len(lines) and start_line < end_line <= len(lines):
            return "\n".join(lines[start_line:end_line])
    return None


def find_block_end(lines: List[str], start_line: int, node: ast.AST) -> int:
    if start_line >= len(lines):
        return start_line + 1
    first_line = lines[start_line]
    base_indent = len(first_line) - len(first_line.lstrip())
    for i in range(start_line + 1, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        current_indent = len(line) - len(line.lstrip())
        if current_indent <= base_indent:
            return i
    return len(lines)


def extract_hash_reference(reference: str, base_path: Optional[Path] = None) -> Optional[str]:
    base = base_path or Path.cwd()
    search_pattern = str(base / "**/*.py")
    for file_path in glob.glob(search_pattern, recursive=True):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
            code = extract_by_function_class(lines, reference)
            if code:
                return code
        except Exception:
            continue
    return None


def extract_html_content(content: str, reference: str) -> Optional[str]:
    content = content.strip()
    if not content:
        return None
    if reference.lower() == "body":
        body_start = content.lower().find("<body")
        if body_start != -1:
            body_tag_end = content.find(">", body_start)
            if body_tag_end != -1:
                body_end = content.lower().rfind("</body>")
                if body_end != -1:
                    extracted = content[body_tag_end + 1 : body_end].strip()
                    return extracted if extracted else content
        return content
    if reference.lower() in ["content", "all", "full"]:
        return content
    if reference.startswith("#"):
        element_id = reference[1:]
        pattern = rf'<[^>]+id\s*=\s*["\']?{re.escape(element_id)}["\']?[^>]*>'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            start_pos = match.start()
            tag_name_match = re.match(r"<(\w+)", match.group())
            if tag_name_match:
                tag_name = tag_name_match.group(1)
                end_pattern = rf"</{tag_name}>"
                end_match = re.search(end_pattern, content[start_pos:], re.IGNORECASE)
                if end_match:
                    extracted = content[start_pos : start_pos + end_match.end()].strip()
                    return extracted if extracted else content
    return content


def get_file_info(
    file_path: str, base_path: Optional[Path] = None, current_file_path: Optional[Path] = None
) -> Optional[dict]:
    try:
        full_path = resolve_path(file_path, base_path, current_file_path)
        if not full_path.exists():
            return None
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
        tree = ast.parse(content)
        functions = []
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "type": ("async function" if isinstance(node, ast.AsyncFunctionDef) else "function"),
                    }
                )
            elif isinstance(node, ast.ClassDef):
                classes.append({"name": node.name, "line": node.lineno})
        return {
            "path": str(full_path),
            "line_count": len(lines),
            "functions": sorted(functions, key=lambda x: x["line"]),
            "classes": sorted(classes, key=lambda x: x["line"]),
        }
    except Exception:
        return None
