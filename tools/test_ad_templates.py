#!/usr/bin/env python3
"""Exercise the restore-safe hidden-div ad template path used by script.js."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = (ROOT / "preview.html").read_text(encoding="utf-8")
JS = (ROOT / "script.js").read_text(encoding="utf-8")
THEME = (ROOT / "sugarcoat_blogger_theme.xml").read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


class SlotFinder(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.article_h2 = 0
        self.cards = 0
        self.templates = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append((tag, attrs))
        classes = attrs.get("class", "").split()
        if "post-card" in classes or "index-post" in classes:
            self.cards += 1
        if tag in {"h1", "h2", "h3"} and any(
            parent[1].get("data-article-body") == "true" or "article-body" in parent[1].get("class", "").split()
            for parent in self.stack
        ):
            if tag == "h2":
                self.article_h2 += 1
        if attrs.get("id") in {"article-middle-ad-template", "list-ad-template"}:
            self.templates[attrs["id"]] = classes

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def main() -> None:
    if "<template" in PREVIEW.lower():
        fail("preview still uses <template>")
    parser = SlotFinder()
    parser.feed(PREVIEW)
    if parser.templates.get("article-middle-ad-template") != ["ad-template"]:
        fail("preview article template is not a hidden ad-template div")
    if parser.templates.get("list-ad-template") != ["ad-template"]:
        fail("preview list template is not a hidden ad-template div")
    if parser.article_h2 < 2:
        fail("preview article needs at least 2 h2 headings for middle-ad insertion")
    if parser.cards < 4:
        fail("preview list needs at least 4 cards for list-ad insertion")

    if "cloneTemplateChild" not in JS:
        fail("script.js missing cloneTemplateChild")
    if "querySelector(\".ad-slot\")" not in JS and "querySelector('.ad-slot')" not in JS:
        fail("script.js missing hidden-div fallback")

    for template_id in ("article-middle-ad-template", "list-ad-template"):
        if f"id='{template_id}'" not in THEME:
            fail(f"theme missing {template_id}")
        if re.search(rf"<template[^>]*id='{template_id}'", THEME):
            fail(f"theme still uses <template> for {template_id}")

    print("ad-template markup tests passed")
    print(f"preview h2 count: {parser.article_h2}")
    print(f"preview card count: {parser.cards}")


if __name__ == "__main__":
    main()
