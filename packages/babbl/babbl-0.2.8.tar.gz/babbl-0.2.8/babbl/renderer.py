"""HTML renderer extends Marko's Renderer class."""

from __future__ import annotations

import html
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, cast
from urllib.parse import quote

from marko import Renderer

from babbl.code_ref import CodeReferenceProcessor
from babbl.defaults import DEFAULT_CSS
from babbl.load import load_file

try:
    from latex2mathml.converter import convert as latex_to_mathml

    LATEX_AVAILABLE = True
except ImportError:
    LATEX_AVAILABLE = False

if TYPE_CHECKING:
    from marko import block, element, inline


class BaseRenderer(ABC, Renderer):
    """Strictly specified Renderer base class that plugs into Marko."""

    @abstractmethod
    def render_paragraph(self, element: block.Paragraph) -> str:
        """Render a paragraph element"""
        pass

    @abstractmethod
    def render_list(self, element: block.List) -> str:
        """Render a list element (ordered or unordered)"""
        pass

    @abstractmethod
    def render_list_item(self, element: block.ListItem) -> str:
        """Render a list item element"""
        pass

    @abstractmethod
    def render_quote(self, element: block.Quote) -> str:
        """Render a blockquote element"""
        pass

    @abstractmethod
    def render_fenced_code(self, element: block.FencedCode) -> str:
        """Render a fenced code block"""
        pass

    @abstractmethod
    def render_code_block(self, element: block.CodeBlock) -> str:
        """Render a code block"""
        pass

    @abstractmethod
    def render_html_block(self, element: block.HTMLBlock) -> str:
        """Render an HTML block"""
        pass

    @abstractmethod
    def render_thematic_break(self, element: block.ThematicBreak) -> str:
        """Render a thematic break (horizontal rule)"""
        pass

    @abstractmethod
    def render_heading(self, element: block.Heading) -> str:
        """Render a heading element"""
        pass

    @abstractmethod
    def render_setext_heading(self, element: block.SetextHeading) -> str:
        """Render a setext heading"""
        pass

    @abstractmethod
    def render_blank_line(self, element: block.BlankLine) -> str:
        """Render a blank line"""
        pass

    @abstractmethod
    def render_link_ref_def(self, element: block.LinkRefDef) -> str:
        """Render a link reference definition"""
        pass

    @abstractmethod
    def render_emphasis(self, element: inline.Emphasis) -> str:
        """Render emphasis (italic) text"""
        pass

    @abstractmethod
    def render_strong_emphasis(self, element: inline.StrongEmphasis) -> str:
        """Render strong emphasis (bold) text"""
        pass

    @abstractmethod
    def render_inline_html(self, element: inline.InlineHTML) -> str:
        """Render inline HTML"""
        pass

    @abstractmethod
    def render_plain_text(self, element: Any) -> str:
        """Render plain text"""
        pass

    @abstractmethod
    def render_link(self, element: inline.Link) -> str:
        """Render a link"""
        pass

    @abstractmethod
    def render_auto_link(self, element: inline.AutoLink) -> str:
        """Render an auto link"""
        pass

    @abstractmethod
    def render_image(self, element: inline.Image) -> str:
        """Render an image"""
        pass

    @abstractmethod
    def render_literal(self, element: inline.Literal) -> str:
        """Render literal text"""
        pass

    @abstractmethod
    def render_raw_text(self, element: inline.RawText) -> str:
        """Render raw text"""
        pass

    @abstractmethod
    def render_line_break(self, element: inline.LineBreak) -> str:
        """Render a line break"""
        pass

    @abstractmethod
    def render_code_span(self, element: inline.CodeSpan) -> str:
        """Render inline code"""
        pass

    @abstractmethod
    def render_table(self, element: Any) -> str:
        """Render a table element"""
        pass

    @abstractmethod
    def render_table_head(self, element: Any) -> str:
        """Render a table head element"""
        pass

    @abstractmethod
    def render_table_body(self, element: Any) -> str:
        """Render a table body element"""
        pass

    @abstractmethod
    def render_table_row(self, element: Any) -> str:
        """Render a table row element"""
        pass

    @abstractmethod
    def render_table_cell(self, element: Any) -> str:
        """Render a table cell element"""
        pass

    @abstractmethod
    def render_table_head_cell(self, element: Any) -> str:
        """Render a table header cell element"""
        pass

    @abstractmethod
    def render_code_reference(self, element: Any) -> str:
        """Render a code reference element"""
        pass


class HTMLRenderer(BaseRenderer):
    """Beautiful HTML renderer with clean styling and semantic classes."""

    def __init__(
        self,
        highlight_syntax: bool = True,
        css_file_path: Optional[Path] = None,
        show_toc: bool = False,
        base_path: Optional[Path] = None,
        current_file_path: Optional[Path] = None,
    ):
        """
        Initialize the HTML renderer.

        Args:
            highlight_syntax: Whether to use Pygments for syntax highlighting
            css_file_path: Path to CSS file
            show_toc: Whether to show table of contents for h1 headings
            base_path: Base path for resolving code reference file paths
            current_file_path: Path to the current markdown file being processed
        """
        super().__init__()
        self.highlight_syntax = highlight_syntax
        self.pygments_formatter = None
        self.show_toc = show_toc
        self.toc_headings: list[tuple[str, str]] = []  # track h1 headings for toc
        self.code_processor = CodeReferenceProcessor(base_path, current_file_path)

        if css_file_path:
            self.base_css = load_file(css_file_path)
        else:
            self.base_css = DEFAULT_CSS

        if self.highlight_syntax:
            try:
                from pygments import highlight  # type: ignore
                from pygments.formatters import HtmlFormatter  # type: ignore
                from pygments.lexers import get_lexer_by_name  # type: ignore

                self.highlight = highlight
                self.get_lexer_by_name = get_lexer_by_name
                self.pygments_formatter = HtmlFormatter(style="friendly")
            except ImportError:
                self.highlight_syntax = False

    @staticmethod
    def _escape_html(raw: str) -> str:
        """Replaces unsafe HTML characters with their escaped equivalents."""
        return html.escape(html.unescape(raw)).replace("&#x27;", "'")

    @staticmethod
    def _escape_html_preserve_mathml(raw: str) -> str:
        """Escape HTML but preserve MathML tags."""
        mathml_tags = []
        placeholder_pattern = "###MATHML_PLACEHOLDER_{}_###"

        def replace_mathml(match):
            mathml_tags.append(match.group(0))
            return placeholder_pattern.format(len(mathml_tags) - 1)

        text = re.sub(r"<math[^>]*>.*?</math>", replace_mathml, raw)
        text = html.escape(html.unescape(text)).replace("&#x27;", "'")

        for i, mathml_tag in enumerate(mathml_tags):
            text = text.replace(placeholder_pattern.format(i), mathml_tag)

        return text

    @staticmethod
    def _escape_url(raw: str) -> str:
        """Escape urls to prevent code injection."""
        return html.escape(quote(html.unescape(raw), safe="/#:()*?=%@+,&"))

    def html(self, element: element.Element, metadata: dict[str, str] | None) -> str:
        """Converts the base element to HTML with full document structure."""
        self.toc_headings = []

        content = super().render(element)
        meta_str = (
            "\n".join(
                f"<meta name={key} content={value}>" for key, value in metadata.items()
            )
            if metadata
            else ""
        )

        toc_html = self.generate_toc() if self.show_toc else ""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{meta_str}
{f"<title>{metadata.get('title', 'Document')}</title>" if metadata else ""}
<style>
{self.get_css()}
</style>
</head>
<body>
<div class="container">
{toc_html}
<main class="content">
<section>
{self.get_header(metadata) if metadata else ""}
{content}
</section>
</main>
</div>
<script>
function toggleCodeRef(id) {{
    const content = document.getElementById(id);
    const header = content.previousElementSibling;
    const toggle = header.querySelector('.code-ref-toggle');
    
    if (content.classList.contains('show')) {{
        content.classList.remove('show');
        toggle.textContent = '▼';
    }} else {{
        content.classList.add('show');
        toggle.textContent = '▲';
    }}
}}
</script>
</body>
</html>"""

    def get_css(self) -> str:
        """Get CSS for the rendered HTML."""
        css = self.base_css

        # add Pygments CSS if available
        if self.highlight_syntax and self.pygments_formatter:
            pygments_css = self.pygments_formatter.get_style_defs(".highlight")
            css += "\n" + pygments_css

        return css

    def get_header(self, metadata: dict[str, str]) -> str:
        """Get the header of the document."""
        meta = metadata.copy()
        res = "<header>\n"
        if "title" in meta:
            title_value = self._process_math_in_metadata(meta["title"])
            res += f'<h1 class="title">{title_value}</h1>\n'
            meta.pop("title")
        res += "<div class='metadata'>\n"
        if "author" in meta:
            author_value = self._process_math_in_metadata(meta["author"])
            res += f'<div class="meta-field">Author: {author_value}</div>\n'
            meta.pop("author")
        if "date" in meta:
            date_value = self._process_math_in_metadata(meta["date"])
            res += f'<div class="meta-field">Date: {date_value}</div>\n'
            meta.pop("date")
        if "summary" in meta:
            summary_value = self._process_math_in_metadata(meta["summary"])
            res += f'<div class="meta-field">Summary: {summary_value}</div>\n'
            meta.pop("summary")
        if "description" in meta:
            description_value = self._process_math_in_metadata(meta["description"])
            res += f'<div class="meta-field">Description: {description_value}</div>\n'
            meta.pop("description")
        if "tags" in meta:
            if isinstance(meta["tags"], list):
                processed_tags = [
                    self._process_math_in_metadata(str(tag)) for tag in meta["tags"]
                ]
                res += (
                    f'<div class="meta-field">Tags: {", ".join(processed_tags)}</div>\n'
                )
            else:
                tags_value = self._process_math_in_metadata(str(meta["tags"]))
                res += f'<div class="meta-field">Tags: {tags_value}</div>\n'
            meta.pop("tags")
        if "categories" in meta:
            categories_value = self._process_math_in_metadata(meta["categories"])
            res += f'<div class="meta-field">Categories: {categories_value}</div>\n'
            meta.pop("categories")
        if "slug" in meta:
            slug_value = self._process_math_in_metadata(meta["slug"])
            res += f'<div class="meta-field">Slug: {slug_value}</div>\n'
            meta.pop("slug")
        if "layout" in meta:
            layout_value = self._process_math_in_metadata(meta["layout"])
            res += f'<div class="meta-field">Layout: {layout_value}</div>\n'
            meta.pop("layout")
        if "draft" in meta:
            draft_value = self._process_math_in_metadata(meta["draft"])
            res += f'<div class="meta-field">Draft: {draft_value}</div>\n'
            meta.pop("draft")
        for key, value in meta.items():
            processed_value = self._process_math_in_metadata(str(value))
            res += f'<div class="meta-field">{key}: {processed_value}</div>\n'
        res += "</div>\n"
        res += "<hr />\n"
        res += "</header>\n"
        return res

    def generate_toc(self) -> str:
        """Generate table of contents HTML from collected h1 headings."""
        if not self.toc_headings:
            return ""

        toc_items = []
        for i, (title, anchor_id) in enumerate(self.toc_headings):
            toc_items.append(
                f'<li><a href="#{anchor_id}" class="toc-link">{title}</a></li>'
            )

        return f"""<aside class="toc">
<nav class="toc-nav">
<ul class="toc-list">
{chr(10).join(toc_items)}
</ul>
</nav>
</aside>"""

    def render_paragraph(self, element: block.Paragraph) -> str:
        children = self.render_children(element)
        if element._tight:  # type: ignore
            return children
        else:
            return f'<p class="paragraph">{children}</p>\n'

    def render_list(self, element: block.List) -> str:
        if element.ordered:
            tag = "ol"
            css_class = "ordered-list"
            extra = f' start="{element.start}"' if element.start != 1 else ""
        else:
            tag = "ul"
            css_class = "unordered-list"
            extra = ""
        return f'<{tag} class="{css_class}"{extra}>\n{self.render_children(element)}</{tag}>\n'

    def render_list_item(self, element: block.ListItem) -> str:
        if len(element.children) == 1 and getattr(element.children[0], "_tight", False):  # type: ignore
            sep = ""
        else:
            sep = "\n"
        return f'<li class="list-item">{sep}{self.render_children(element)}</li>\n'

    def render_quote(self, element: block.Quote) -> str:
        return f'<blockquote class="blockquote">\n{self.render_children(element)}</blockquote>\n'

    def render_fenced_code(self, element: block.FencedCode) -> str:
        code_content = element.children[0].children  # type: ignore

        if self.highlight_syntax and element.lang and self.pygments_formatter:
            try:
                lexer = self.get_lexer_by_name(element.lang)
                highlighted_code = self.highlight(code_content, lexer, self.pygments_formatter)  # type: ignore
                # ensure proper class structure
                highlighted_code = highlighted_code.replace(
                    '<div class="highlight"><pre>',
                    '<div class="highlight"><pre class="code-block">',
                )
                return highlighted_code + "\n"
            except:
                # fallback to plain code block
                pass

        lang_class = (
            f' class="language-{self._escape_html(element.lang)}"'
            if element.lang
            else ""
        )
        escaped_code = html.escape(code_content)
        return (
            f'<pre class="code-block"{lang_class}><code>{escaped_code}</code></pre>\n'
        )

    def render_code_block(self, element: block.CodeBlock) -> str:
        return self.render_fenced_code(cast("block.FencedCode", element))

    def render_html_block(self, element: block.HTMLBlock) -> str:
        return element.body

    def render_thematic_break(self, element: block.ThematicBreak) -> str:
        return "<hr />\n"

    def render_heading(self, element: block.Heading) -> str:
        css_class = f"heading-{element.level}"
        heading_text = self.render_children(element)

        clean_heading_text = re.sub(r"<math[^>]*>.*?</math>", "", heading_text)
        anchor_id = self._create_anchor_id(clean_heading_text)

        # track h1 headings for toc
        if (element.level == 1 or element.level == 2) and self.show_toc:
            self.toc_headings.append((heading_text, anchor_id))

        return f'<h{element.level} id="{anchor_id}" class="{css_class}">{heading_text}</h{element.level}>\n'

    def _create_anchor_id(self, text: str) -> str:
        """Create a URL-friendly anchor ID from heading text."""
        clean_text = re.sub(r"<[^>]+>", "", text)
        clean_text = html.unescape(clean_text)

        anchor_id = re.sub(r"[^\w\s-]", "", clean_text.lower())
        anchor_id = re.sub(r"[-\s]+", "-", anchor_id)
        anchor_id = anchor_id.strip("-")

        base_id = anchor_id
        counter = 1
        while any(existing_id == anchor_id for _, existing_id in self.toc_headings):
            anchor_id = f"{base_id}-{counter}"
            counter += 1

        return anchor_id

    def _process_latex_math_text(self, text: str) -> str:
        """Process LaTeX math expressions in raw text before HTML escaping."""
        if not LATEX_AVAILABLE:
            return text

        def replace_inline_math(match):
            latex_code = match.group(1)
            try:
                mathml = latex_to_mathml(latex_code)
                return mathml
            except Exception:
                return match.group(0)

        def replace_display_math(match):
            latex_code = match.group(1)
            try:
                mathml = latex_to_mathml(latex_code)
                return f'<div class="math-display">{mathml}</div>'
            except Exception:
                return match.group(0)

        text = re.sub(r"\$([^$]+)\$", replace_inline_math, text)
        text = re.sub(r"\$\$([^$]+)\$\$", replace_display_math, text)

        return text

    def _process_math_in_metadata(self, text: str) -> str:
        """Process LaTeX math expressions in metadata values and escape HTML."""
        if not LATEX_AVAILABLE:
            return self._escape_html(text)

        processed_text = self._process_latex_math_text(text)
        return self._escape_html_preserve_mathml(processed_text)

    def render_setext_heading(self, element: block.SetextHeading) -> str:
        return self.render_heading(cast("block.Heading", element))

    def render_blank_line(self, element: block.BlankLine) -> str:
        return ""

    def render_link_ref_def(self, element: block.LinkRefDef) -> str:
        return ""

    def render_emphasis(self, element: inline.Emphasis) -> str:
        return f'<em class="emphasis">{self.render_children(element)}</em>'

    def render_strong_emphasis(self, element: inline.StrongEmphasis) -> str:
        return f'<strong class="strong">{self.render_children(element)}</strong>'

    def render_inline_html(self, element: inline.InlineHTML) -> str:
        return cast(str, element.children)

    def render_plain_text(self, element: Any) -> str:
        if isinstance(element.children, str):
            text = element.children
            if LATEX_AVAILABLE:
                text = self._process_latex_math_text(text)
                return self._escape_html_preserve_mathml(text)
            return self._escape_html(text)
        return self.render_children(element)

    def render_link(self, element: inline.Link) -> str:
        template = '<a href="{}" class="link"{}>{}</a>'
        title = f' title="{self._escape_html(element.title)}"' if element.title else ""
        url = self._escape_url(element.dest)
        body = self.render_children(element)
        return template.format(url, title, body)

    def render_auto_link(self, element: inline.AutoLink) -> str:
        return self.render_link(cast("inline.Link", element))

    def render_image(self, element: inline.Image) -> str:
        template = '<img src="{}" alt="{}" class="image"{} />'
        title = f' title="{self._escape_html(element.title)}"' if element.title else ""
        url = self._escape_url(element.dest)
        render_func = self.render
        self.render = self.render_plain_text  # type: ignore
        body = self.render_children(element)
        self.render = render_func  # type: ignore
        return template.format(url, body, title)

    def render_literal(self, element: inline.Literal) -> str:
        return self.render_raw_text(cast("inline.RawText", element))

    def render_raw_text(self, element: inline.RawText) -> str:
        text = element.children
        if LATEX_AVAILABLE:
            text = self._process_latex_math_text(text)
            return self._escape_html_preserve_mathml(text)
        return self._escape_html(text)

    def render_line_break(self, element: inline.LineBreak) -> str:
        if element.soft:
            return "\n"
        return "<br />\n"

    def render_code_span(self, element: inline.CodeSpan) -> str:
        escaped_code = html.escape(cast(str, element.children))
        return f'<code class="inline-code">{escaped_code}</code>'

    def render_table(self, element: Any) -> str:
        """Render a table element."""
        # Handle our custom Table element
        if hasattr(element, "headers") and hasattr(element, "rows"):
            html = '<div class="table-container">\n<table class="table">\n'

            html += "<thead>\n<tr>\n"
            for header in element.headers:
                html += f"<th>{self._escape_html(header)}</th>\n"
            html += "</tr>\n</thead>\n"

            html += "<tbody>\n"
            for row in element.rows:
                html += "<tr>\n"
                for cell in row:
                    html += f"<td>{self._escape_html(cell)}</td>\n"
                html += "</tr>\n"
            html += "</tbody>\n"

            html += "</table>\n</div>\n"
            return html

        # Fallback to generic table rendering
        return f'<div class="table-container">\n<table class="table">\n{self.render_children(element)}</table>\n</div>\n'

    def render_table_head(self, element: Any) -> str:
        """Render a table head element."""
        return f"<thead>\n{self.render_children(element)}</thead>\n"

    def render_table_body(self, element: Any) -> str:
        """Render a table body element."""
        return f"<tbody>\n{self.render_children(element)}</tbody>\n"

    def render_table_row(self, element: Any) -> str:
        """Render a table row element."""
        return f"<tr>\n{self.render_children(element)}</tr>\n"

    def render_table_cell(self, element: Any) -> str:
        """Render a table cell element."""
        return f"<td>{self.render_children(element)}</td>\n"

    def render_table_head_cell(self, element: Any) -> str:
        """Render a table header cell element."""
        return f"<th>{self.render_children(element)}</th>\n"

    def render_code_reference(self, element: Any) -> str:
        """Render a code reference element."""
        # extract code from the referenced file
        syntax_type = getattr(element, "syntax_type", "old")
        code = self.code_processor.extract_code(
            element.file_path, element.reference, syntax_type
        )

        if not code:
            if syntax_type == "hash":
                error_msg = f"Code reference not found: #{element.reference}"
            else:
                error_msg = f"Code reference not found: {element.file_path} - {element.reference}"
            return f'<div class="code-ref-error">{error_msg}</div>\n'

        # Check if this is an HTML file - if so, render as HTML directly
        if element.file_path and element.file_path.lower().endswith(".html"):
            return f'<div class="html-inclusion">\n{code}\n</div>\n'

        # create a unique id for the dropdown
        import uuid

        dropdown_id = f"code-ref-{uuid.uuid4().hex[:8]}"

        # escape the code for HTML
        escaped_code = html.escape(code)

        # determine language for syntax highlighting
        if element.file_path:
            file_ext = Path(element.file_path).suffix.lower()
        else:
            file_ext = ".py"  # default for hash references

        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "c",
            ".cs": "csharp",
            ".php": "php",
            ".rb": "ruby",
            ".go": "go",
            ".rs": "rust",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".sh": "bash",
            ".bash": "bash",
            ".zsh": "bash",
            ".fish": "bash",
            ".sql": "sql",
            ".html": "html",
            ".css": "css",
            ".scss": "scss",
            ".sass": "sass",
            ".less": "less",
            ".xml": "xml",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".ini": "ini",
            ".cfg": "ini",
            ".conf": "ini",
            ".md": "markdown",
            ".txt": "text",
        }
        language = lang_map.get(file_ext, "text")

        # apply syntax highlighting if available
        if self.highlight_syntax and self.pygments_formatter:
            try:
                lexer = self.get_lexer_by_name(language)
                highlighted_code = self.highlight(code, lexer, self.pygments_formatter)
                # ensure proper class structure
                highlighted_code = highlighted_code.replace(
                    '<div class="highlight"><pre>',
                    '<div class="highlight"><pre class="code-block">',
                )
                code_html = highlighted_code
            except:
                # fallback to plain code
                code_html = f'<pre class="code-block language-{language}"><code>{escaped_code}</code></pre>'
        else:
            code_html = f'<pre class="code-block language-{language}"><code>{escaped_code}</code></pre>'

        # Generate appropriate title based on syntax type
        if syntax_type == "hash":
            title = f"#{element.reference}"
        else:
            title = f"{element.file_path} - {element.reference}"

        return f"""<div class="code-reference">
<div class="code-ref-header" onclick="toggleCodeRef('{dropdown_id}')">
<span class="code-ref-title">{title}</span>
<span class="code-ref-toggle">▼</span>
</div>
<div class="code-ref-content" id="{dropdown_id}">
{code_html}
</div>
</div>\n"""
