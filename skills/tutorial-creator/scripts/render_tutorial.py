#!/usr/bin/env python3
"""
Render tutorial Markdown files to companion HTML files.

The renderer intentionally supports a practical Markdown subset using only the
Python standard library. Keep the Markdown files as the source of truth.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "assets" / "tutorial-template.html"


def slugify_heading(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def html_href_for_markdown_target(href: str) -> str:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href) or href.startswith("#"):
        return href

    match = re.match(r"^([^#?]+)\.md([#?].*)?$", href)
    if not match:
        return href
    suffix = match.group(2) or ""
    return f"{match.group(1)}.html{suffix}"


def inline_markdown(text: str) -> str:
    placeholders: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\0{len(placeholders) - 1}\0"

    protected = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(protected)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: (
            f'<a href="{html.escape(html_href_for_markdown_target(m.group(2)), quote=True)}">'
            f"{m.group(1)}</a>"
        ),
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"\0{index}\0", value)
    return escaped


def close_list(open_list: str | None) -> tuple[str, str | None]:
    if not open_list:
        return "", None
    return f"</{open_list}>\n", None


def render_code_block(code_lines: list[str], code_lang: str) -> str:
    class_attr = (
        f' class="language-{html.escape(code_lang, quote=True)}"' if code_lang else ""
    )
    numbered_lines = "\n".join(
        '<span class="code-line">'
        f'<span class="line-number">{line_number}</span>'
        f'<span class="line-code">{html.escape(line)}</span>'
        "</span>"
        for line_number, line in enumerate(code_lines, start=1)
    )
    return f'<pre class="code-block"><code{class_attr}>{numbered_lines}</code></pre>\n'


def markdown_to_html(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    open_list: str | None = None
    in_code = False
    code_lines: list[str] = []
    code_lang = ""

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>\n")
            paragraph = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        fence = re.match(r"^```([A-Za-z0-9_-]+)?\s*$", line)
        if fence:
            if in_code:
                output.append(render_code_block(code_lines, code_lang))
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                flush_paragraph()
                closed, open_list = close_list(open_list)
                output.append(closed)
                in_code = True
                code_lang = fence.group(1) or ""
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line.strip():
            flush_paragraph()
            closed, open_list = close_list(open_list)
            output.append(closed)
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            closed, open_list = close_list(open_list)
            output.append(closed)
            level = len(heading.group(1))
            text = heading.group(2).strip()
            output.append(
                f'<h{level} id="{slugify_heading(text)}">{inline_markdown(text)}</h{level}>\n',
            )
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", line)
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph()
            tag = "ul" if unordered else "ol"
            content = (unordered or ordered).group(1)
            if open_list != tag:
                closed, open_list = close_list(open_list)
                output.append(closed)
                output.append(f"<{tag}>\n")
                open_list = tag
            output.append(f"<li>{inline_markdown(content)}</li>\n")
            continue

        quote = re.match(r"^>\s?(.+)$", line)
        if quote:
            flush_paragraph()
            closed, open_list = close_list(open_list)
            output.append(closed)
            output.append(
                f"<blockquote>{inline_markdown(quote.group(1))}</blockquote>\n",
            )
            continue

        paragraph.append(line.strip())

    if in_code:
        raise ValueError("Unclosed Markdown code fence")
    flush_paragraph()
    closed, open_list = close_list(open_list)
    output.append(closed)
    return "".join(output)


def page_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return re.sub(r"`([^`]+)`", r"\1", match.group(1)).strip()
    return fallback


def render_page_navigation(markdown_path: Path, all_markdown_paths: list[Path]) -> str:
    if len(all_markdown_paths) <= 1:
        return ""

    current_index = all_markdown_paths.index(markdown_path)
    previous_path = all_markdown_paths[current_index - 1] if current_index > 0 else None
    next_path = (
        all_markdown_paths[current_index + 1]
        if current_index < len(all_markdown_paths) - 1
        else None
    )
    home_path = all_markdown_paths[0]

    def link(path: Path, rel: str, fallback_label: str) -> str:
        title = page_title(path.read_text(encoding="utf-8"), path.stem)
        return (
            f'<a class="page-nav-link page-nav-{rel}" rel="{rel}" '
            f'href="{path.with_suffix(".html").name}">'
            f'<span>{fallback_label}</span>'
            f"<strong>{html.escape(title)}</strong>"
            "</a>"
        )

    previous_html = (
        link(previous_path, "prev", "Previous")
        if previous_path
        else '<span class="page-nav-spacer" aria-hidden="true"></span>'
    )
    home_html = link(home_path, "home", "Home")
    next_html = (
        link(next_path, "next", "Next")
        if next_path
        else '<span class="page-nav-spacer" aria-hidden="true"></span>'
    )
    return f"""<nav class="page-nav" aria-label="Tutorial navigation">
{previous_html}
{home_html}
{next_html}
</nav>"""


def render_page(markdown_path: Path, all_markdown_paths: list[Path]) -> str:
    markdown = markdown_path.read_text(encoding="utf-8")
    title = page_title(markdown, markdown_path.stem.replace("-", " ").title())
    body = markdown_to_html(markdown)
    page_navigation = render_page_navigation(markdown_path, all_markdown_paths)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("{{title}}", html.escape(title))
        .replace("{{header_nav}}", page_navigation)
        .replace("{{footer_nav}}", page_navigation)
        .replace("{{body}}", body)
    )


def render_directory(topic_dir: Path) -> list[Path]:
    if not topic_dir.exists() or not topic_dir.is_dir():
        raise SystemExit(f"Topic directory does not exist: {topic_dir}")

    markdown_paths = sorted(path for path in topic_dir.glob("*.md") if path.is_file())
    markdown_paths.sort(key=lambda path: (path.name != "index.md", path.name))
    if not markdown_paths:
        raise SystemExit(f"No Markdown files found in: {topic_dir}")

    html_paths: list[Path] = []
    for markdown_path in markdown_paths:
        html_path = markdown_path.with_suffix(".html")
        html_path.write_text(
            render_page(markdown_path, markdown_paths),
            encoding="utf-8",
        )
        html_paths.append(html_path)
    return html_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render tutorial Markdown files to matching HTML files.",
    )
    parser.add_argument(
        "topic_dir",
        type=Path,
        help="Directory containing tutorial .md files",
    )
    args = parser.parse_args()

    html_paths = render_directory(args.topic_dir)
    for html_path in html_paths:
        print(html_path)


if __name__ == "__main__":
    main()
