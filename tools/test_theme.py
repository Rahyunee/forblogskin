#!/usr/bin/env python3
"""Sanity checks for the generated Blogger theme XML."""
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build_theme.py"
THEME = ROOT / "sugarcoat_blogger_theme.xml"
JS = ROOT / "script.js"

WIDGET_ID = re.compile(r"[A-Za-z]+\d+")
REQUIRED = [
    "ea6ff9bb5eb9b747dfe69fbe5d123c620bcf5dc8",
    "G-KDJJ18MT54",
    "ca-pub-6692939836499331",
    "7633913202",
    "1008345394",
    "HTML101",
    "HTML108",
    "commentPicker",
    "threadedComments",
    "ad-article-top",
    "article-middle-ad-template",
]


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def test_build() -> str:
    result = subprocess.run([sys.executable, str(BUILD)], check=True, capture_output=True, text=True)
    xml = THEME.read_text(encoding="utf-8")
    if "Wrote" not in result.stdout:
        fail("build script did not report output path")
    return xml


def test_restore_rules(xml: str) -> None:
    if "HTMLAd" in xml:
        fail("legacy HTMLAd* widget ids remain")
    if "super." in xml:
        fail("super.* includes remain")
    if re.search(r"<template[\s>]", xml):
        fail("<template> tags remain")
    if re.search(r"<b:section\b[^>]*/>", xml):
        fail("self-closing b:section remains")
    head, body = xml.split("</head>", 1)
    if "<b:defaultmarkups>" not in head:
        fail("b:defaultmarkups missing from head")
    if "<b:defaultmarkups>" in body:
        fail("b:defaultmarkups still in body")
    ids = re.findall(r"<b:widget[^>]*\bid='([^']+)'", xml)
    if not ids:
        fail("no widgets found")
    bad = [widget_id for widget_id in ids if not WIDGET_ID.fullmatch(widget_id)]
    if bad:
        fail("invalid widget ids: " + ", ".join(bad))
    for token in REQUIRED:
        if token not in xml:
            fail(f"missing required token {token!r}")
    if "easypress" in xml.lower() or "adsensefarm" in xml.lower():
        fail("Easypress/adsensefarm leftover in apply XML")
    if xml.count("id='HTML101'") != 1:
        fail("HTML101 must appear exactly once")
    if "id='HTML1'" in xml:
        fail("HTML1 collides with the live theme gadget")


def test_xml_shape(xml: str) -> None:
    # Blogger GML is not strict XML; still catch unmatched tags in the gadget shell.
    if xml.count("<head>") != 1 or xml.count("</head>") != 1:
        fail("head tag mismatch")
    if xml.count("<body>") != 1 or xml.count("</body>") != 1:
        fail("body tag mismatch")
    if xml.count("<b:widget ") != xml.count("</b:widget>"):
        fail("widget open/close mismatch")
    if xml.count("<b:section") != xml.count("</b:section>"):
        fail("section open/close mismatch")
    if xml.count("<b:includable") != xml.count("</b:includable>"):
        fail("includable open/close mismatch")


def test_clone_template_child() -> None:
    js = JS.read_text(encoding="utf-8")
    if "template.content && template.content.firstElementChild" not in js:
        fail("cloneTemplateChild missing template.content path")
    if 'template.querySelector(".ad-slot")' not in js:
        fail("cloneTemplateChild missing hidden-div fallback")
    # Mirror the hidden-div fallback used after restore-safe markup.
    wrapper = ET.fromstring(
        "<div id='article-middle-ad-template' class='ad-template'>"
        "<div class='ad-slot ad-slot--article-middle' data-auto-ad='middle'>"
        "<span class='ad-label'>AD</span>"
        "</div></div>"
    )
    child = wrapper.find(".//*[@class]")
    slot = None
    for node in wrapper.iter():
        classes = node.attrib.get("class", "").split()
        if "ad-slot" in classes:
            slot = node
            break
    if slot is None or child is None:
        fail("ad template fixture missing .ad-slot")
    clone = ET.fromstring(ET.tostring(slot, encoding="unicode"))
    if "ad-slot--article-middle" not in clone.attrib.get("class", ""):
        fail("cloned ad slot lost class")


def test_gtag_braces(xml: str) -> None:
    if "function gtag(){dataLayer.push(arguments);}" not in xml:
        fail("gtag function was not emitted with real braces")
    if "function gtag(){{" in xml:
        fail("python f-string braces leaked into XML")


def main() -> None:
    xml = test_build()
    test_restore_rules(xml)
    test_xml_shape(xml)
    test_clone_template_child()
    test_gtag_braces(xml)
    widget_count = len(re.findall(r"<b:widget ", xml))
    print("theme tests passed")
    print(f"widgets: {widget_count}")
    print(f"size: {len(xml.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
