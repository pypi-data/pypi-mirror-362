"""CSS configuration system for babbl."""

DEFAULT_CSS = """body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    max-width: 750px;
    margin: 0 auto;
    padding: 1.5rem;
    color: #333;
    background-color: #fff;
}

section {
    padding: 0;
}

.title {
    font-size: 2.0rem;
    margin-top: 1.0rem;
    margin-bottom: 0.0rem;
    color: #333;
    font-weight: 600;
}

.heading-1 { 
    font-size: 1.6rem; 
    margin-top: 1.0rem; 
    margin-bottom: 0.5rem; 
    color: #333;
    font-weight: 600;
}

.heading-2 { 
    font-size: 1.4rem; 
    margin-top: 1rem; 
    margin-bottom: 0.5rem; 
    color: #333;
    font-weight: 600;
}

.heading-3 { 
    font-size: 1.2rem; 
    margin-top: 1.0rem; 
    margin-bottom: 0.5rem; 
    color: #333;
    font-weight: 600;
}

.heading-4, .heading-5, .heading-6 { 
    font-size: 1rem; 
    margin-top: 1rem; 
    margin-bottom: 0.5rem; 
    color: #333;
    font-weight: 600;
}

.paragraph { 
    margin-bottom: 1rem; 
    text-align: left;
    font-size: .9rem;
}

.code-block { 
    background: #f5f5f5; 
    padding: 1rem; 
    border: none;
    overflow-x: auto;
    margin: 0;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.4;
    color: #333;
}

.inline-code { 
    background: #f5f5f5; 
    padding: 0.15rem 0.3rem; 
    border: none;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    font-size: 0.75rem;
    color: #333;
}

.link { 
    color: #0066cc; 
    text-decoration: none; 
}

.link:hover { 
    text-decoration: underline;
}

.image { 
    max-width: 100%; 
    height: auto; 
    margin: 1rem 0; 
    border: none;
}

.unordered-list, .ordered-list { 
    margin: 1rem 0; 
    padding-left: 2rem; 
}

.list-item { 
    margin-bottom: 0.5rem; 
    line-height: 1.6;
    font-size: .9rem;
}

.blockquote { 
    border-left: 3px solid #ddd; 
    padding-left: 1rem; 
    margin: 0.5rem 0; 
    font-style: italic;
    color: #666;
    background: none;
    padding: 0.25rem 0.5rem;
    font-size: 0.9rem;
}

.strong { 
    font-weight: 600; 
    color: #333;
}

.emphasis { 
    font-style: italic; 
    color: #333;
}

.metadata {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

.meta-field {
    margin-bottom: 0.25rem;
    line-height: 1.2rem;
}

.meta-field:last-child {
    margin-bottom: 0;
}

hr {
    border: none;
    height: 1px;
    background: #ddd;
    margin: 1.5rem 0;
}

/* Table Styles */
.table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.9rem;
    background: #fff;
    border: 1px solid #ddd;
}

.table th {
    background: #f8f9fa;
    border: 1px solid #ddd;
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
    color: #333;
}

.table td {
    border: 1px solid #ddd;
    padding: 0.75rem;
    text-align: left;
    vertical-align: top;
}

.table tr:nth-child(even) {
    background: #f8f9fa;
}

.table tr:hover {
    background: #f1f3f4;
}

.table-container {
    overflow-x: auto;
    margin: 1rem 0;
}

.container {
    position: relative;
    max-width: 750px;
    margin: 0 auto;
}

.toc {
    position: fixed;
    top: 11.75rem;
    left: calc(50% - 625px);
    width: 200px;
    max-height: calc(100vh - 8rem);
    overflow-y: auto;
}

.toc-nav {
    margin: 0;
}

.toc-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #ddd;
}

.toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.toc-list li {
    margin-bottom: 0.75rem;
}

.toc-link {
    display: block;
    padding: 0.25rem 0;
    color: #666;
    text-decoration: none;
    font-size: 0.85rem;
    line-height: 1.4;
    text-align: right;
    transition: color 0.2s ease;
}

.toc-link:hover {
    color: #0066cc;
    text-decoration: none;
}

.content {
    width: 100%;
}

/* Code Reference Styles */
.code-reference {
    margin: 1rem 0;
    border: 1px solid #ddd;
    border-radius: 6px;
    overflow: hidden;
    background: #fff;
}

.code-ref-header {
    background: #f8f9fa;
    padding: 0.75rem .9rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background-color 0.2s ease;
}

.code-ref-header:hover {
    background: #e9ecef;
}

.code-ref-title {
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    font-size: 0.75rem;
    color: #495057;
    font-weight: 500;
}

.code-ref-toggle {
    font-size: 0.75rem;
    color: #6c757d;
    transition: transform 0.2s ease;
}

.code-ref-content {
    display: none;
    padding: 0;
    background: #fff;
}

.code-ref-content.show {
    display: block;
}

.code-ref-error {
    background: #f8d7da;
    color: #721c24;
    padding: 0.75rem 1rem;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
    font-size: 0.75rem;
    margin: 1rem 0;
}

/* HTML Inclusion Styles */
.html-inclusion {
    margin: 1rem 0;
    border: none;
    border-radius: 0;
    overflow: auto;
    background: transparent;
    padding: 0;
}

/* Math Styles */
.math-inline {
    display: inline;
    font-family: 'Times New Roman', Times, serif;
}

.math-display {
    display: block;
    text-align: center;
    margin: 1rem 0;
    font-family: 'Times New Roman', Times, serif;
}

/* MathML styling */
math {
    font-family: 'Times New Roman', Times, serif;
}

/* Responsive design for mobile */
@media (max-width: 768px) {
    .toc {
        position: static;
        width: auto;
        max-height: none;
        margin-bottom: 1rem;
    }
    
    body {
        padding: 1rem;
    }
}
"""
