# Babbl

A modern markdown-to-HTML converter designed for research blog posts with support for tables, code references, and beautiful styling.

## Features

- **Clean HTML Output**: Semantic HTML with responsive CSS styling
- **Table Support**: Full markdown table rendering with clean styling
- **Code References**: Include code snippets from files using simple syntax
- **Syntax Highlighting**: Pygments integration for code blocks
- **Table of Contents**: Auto-generated TOC for document navigation
- **Frontmatter Support**: YAML metadata in markdown files
- **Extensible**: Built with Marko parser for easy customization

## Installation

```bash
pip install babbl
```

## Quick Start

### Render a single file
```bash
babbl render document.md
```

### Build multiple files
```bash
babbl build ./docs --output-dir ./public
```

### With custom styling
```bash
babbl render document.md --css custom.css --toc
```

## Usage

### Python API

```python
from babbl import BabblParser, HTMLRenderer

parser = BabblParser()
renderer = HTMLRenderer()

with open("document.md", "r") as f:
    content = f.read()

document = parser.parse(content)
html = renderer.html(document, metadata={})
```

### Code References

Reference code from files using simple syntax:

```markdown
#function_name
[Description](path/to/file.py#function_name)
[Line 15](path/to/file.py#L15)
[Lines 10-20](path/to/file.py#L10-L20)
```

### Tables

Standard markdown table syntax:

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Frontmatter

YAML metadata at the beginning of files:

```markdown
---
title: "My Document"
author: "Author Name"
date: "2024-01-01"
---

# Content starts here
```

## CLI Commands

### `babbl render`
Render a single markdown file to HTML.

**Options:**
- `--output, -o`: Output file path
- `--css`: Custom CSS file
- `--toc`: Generate table of contents
- `--base-path`: Base path for code references

### `babbl build`
Build multiple markdown files in a directory.

**Options:**
- `--output-dir, -o`: Output directory
- `--pattern`: File pattern (default: `*.md`)
- `--recursive, -r`: Process subdirectories
- `--css`: Custom CSS file
- `--toc`: Generate table of contents
- `--base-path`: Base path for code references

## License

MIT License