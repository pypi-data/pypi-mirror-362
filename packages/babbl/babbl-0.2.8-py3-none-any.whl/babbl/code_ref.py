"""Code reference processor for extracting code from Python files."""

import ast
import re
from pathlib import Path
from typing import List, Optional, Tuple


class CodeReferenceProcessor:
    """Process code references and extract code from Python files."""

    def __init__(
        self, base_path: Optional[Path] = None, current_file_path: Optional[Path] = None
    ):
        """
        Initialize the code reference processor.

        Args:
            base_path: Base path for resolving relative file paths (fallback)
            current_file_path: Path to the current markdown file being processed
        """
        self.base_path = base_path or Path.cwd()
        self.current_file_path = current_file_path
        self.current_file_cache: dict[str, str] = {}  # cache for current file analysis

    def extract_code(
        self, file_path: str, reference: str, syntax_type: str = "link"
    ) -> Optional[str]:
        """
        Extract code from a file based on the reference.

        Args:
            file_path: Path to the Python file (can be empty for hash references)
            reference: Reference string (function name, class name, line numbers, etc.)
            syntax_type: Type of syntax used ("link", "hash")

        Returns:
            Extracted code string or None if not found
        """
        try:
            # Handle hash references that don't specify a file
            if syntax_type == "hash" and not file_path:
                # For hash references without file path, search in common locations
                return self._extract_hash_reference(reference)

            full_path = self._resolve_path(file_path)
            if not full_path.exists():
                return None

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Handle HTML files differently
            if file_path.lower().endswith(".html"):
                return self._extract_html_content(content, reference)

            lines = content.split("\n")

            # try different reference types
            code = self._extract_by_function_class(lines, reference)
            if code:
                return code

            code = self._extract_by_line_numbers(lines, reference)
            if code:
                return code

            code = self._extract_by_line_range(lines, reference)
            if code:
                return code

            return None

        except Exception:
            return None

    def _resolve_path(self, file_path: str) -> Path:
        """Resolve file path relative to current markdown file or base path."""
        path = Path(file_path)
        if path.is_absolute():
            return path

        # If we have a current file path, resolve relative to its directory
        if self.current_file_path:
            relative_path = self.current_file_path.parent / path
            if relative_path.exists():
                return relative_path

        # Fallback to base path
        return self.base_path / path

    def _extract_by_function_class(
        self, lines: List[str], reference: str
    ) -> Optional[str]:
        """Extract code by function or class name using AST."""
        try:
            content = "\n".join(lines)
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    if node.name == reference:
                        start_line = node.lineno - 1  # ast uses 1-based indexing
                        end_line = (
                            node.end_lineno
                            if hasattr(node, "end_lineno")
                            else start_line + 1
                        )

                        # find the actual end of the function/class
                        end_line = self._find_block_end(lines, start_line, node)

                        return "\n".join(lines[start_line:end_line])

            return None
        except Exception:
            return None

    def _extract_by_line_numbers(
        self, lines: List[str], reference: str
    ) -> Optional[str]:
        """Extract code by specific line numbers."""
        # pattern: line 5, line 10, etc.
        line_match = re.match(r"line\s+(\d+)", reference, re.IGNORECASE)
        if line_match:
            line_num = int(line_match.group(1)) - 1  # convert to 0-based
            if 0 <= line_num < len(lines):
                return lines[line_num]
        return None

    def _extract_by_line_range(self, lines: List[str], reference: str) -> Optional[str]:
        """Extract code by line range."""
        # pattern: lines 5-10, lines 5:10, etc.
        range_match = re.match(r"lines?\s+(\d+)[-:]\s*(\d+)", reference, re.IGNORECASE)
        if range_match:
            start_line = int(range_match.group(1)) - 1  # convert to 0-based
            end_line = int(range_match.group(2))  # keep 1-based for slicing

            if 0 <= start_line < len(lines) and start_line < end_line <= len(lines):
                return "\n".join(lines[start_line:end_line])
        return None

    def _find_block_end(self, lines: List[str], start_line: int, node: ast.AST) -> int:
        """Find the end of a code block by analyzing indentation."""
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

    def _extract_hash_reference(self, reference: str) -> Optional[str]:
        """
        Extract code for a hash reference by searching in common locations.

        Args:
            reference: The reference name (function, class, etc.)

        Returns:
            Extracted code string or None if not found
        """
        # Common Python file locations to search
        search_paths = [
            self.base_path / "**/*.py",
        ]

        import glob

        for pattern in search_paths:
            for file_path in glob.glob(str(pattern), recursive=True):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        lines = content.split("\n")

                    # Try to find the reference in this file
                    code = self._extract_by_function_class(lines, reference)
                    if code:
                        return code

                except Exception:
                    continue

        return None

    def _extract_html_content(self, content: str, reference: str) -> Optional[str]:
        """Extract HTML content based on the reference."""
        if not content:
            return None

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
            import re

            pattern = rf'<[^>]+id\s*=\s*["\']?{re.escape(element_id)}["\']?[^>]*>'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                start_pos = match.start()
                tag_name_match = re.match(r"<(\w+)", match.group())
                if tag_name_match:
                    tag_name = tag_name_match.group(1)
                    end_pattern = rf"</{tag_name}>"
                    end_match = re.search(
                        end_pattern, content[start_pos:], re.IGNORECASE
                    )
                    if end_match:
                        extracted = content[
                            start_pos : start_pos + end_match.end()
                        ].strip()
                        return extracted if extracted else content

        return content

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get information about a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            Dictionary with file information or None if file not found
        """
        try:
            full_path = self._resolve_path(file_path)
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
                            "type": (
                                "async function"
                                if isinstance(node, ast.AsyncFunctionDef)
                                else "function"
                            ),
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
