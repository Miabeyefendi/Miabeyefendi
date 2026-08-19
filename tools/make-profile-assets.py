#!/usr/bin/env python3
"""
Generate the profile banner and the section headers.

Everything here is written into the repository as a static SVG. Nothing is
fetched from a third-party rendering service at view time, so the page cannot
break because someone else's server went away. The palette is the one in
.Git Templates/assets/STYLE.md, so the profile and the project repositories
look like they belong to the same person.

    python tools/make-profile-assets.py
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

ACCENT_A = "#A78BFA"
ACCENT_B = "#0EA5E9"
SUCCESS = "#22C55E"
INK = "#0B0E14"
PAPER = "#FFFFFF"
TEXT_DARK = "#E6EDF3"
TEXT_LIGHT = "#1F2328"
MUTED_DARK = "#8B949E"
MUTED_LIGHT = "#57606A"
BORDER_DARK = "#30363D"
BORDER_LIGHT = "#D0D7DE"

FONT = ("ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',"
        "Roboto,Helvetica,Arial,sans-serif")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

NARROW = "iljItf.,:;'!|()[]"
WIDE = "mMW@"
UPPER = "ABCDEFGHKNOPQRSUVXYZ"


def text_width(label, size, tracking=0.0):
    total = 0.0
    for ch in label:
        if ch == " ":
            total += 0.28
        elif ch in NARROW:
            total += 0.31
        elif ch in WIDE:
            total += 0.90
        elif ch in UPPER:
            total += 0.68
        else:
            total += 0.55
    return round(total * size + tracking * max(len(label) - 1, 0), 1)


def banner(dark):
    """The header image. 1000x260, rounded, gradient rule, name and role."""
    bg = INK if dark else PAPER
    fg = TEXT_DARK if dark else TEXT_LIGHT
    muted = MUTED_DARK if dark else MUTED_LIGHT
    border = BORDER_DARK if dark else BORDER_LIGHT
    dot = "#1B2130" if dark else "#EDF1F5"

    name = "Miabeyefendi"
    role = "Automation and scraping tools, built solo"
    tags = "Python  ·  C#  ·  C++  ·  JavaScript  ·  Playwright"

    name_w = text_width(name, 58, 1.5)
    role_w = text_width(role, 19)
    tags_w = text_width(tags, 14, 0.6)

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="260" '
        'viewBox="0 0 1000 260" role="img" '
        'aria-label="Miabeyefendi, automation and scraping tools, built solo">'
        '<defs>'
        '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
        '<stop offset="1" stop-color="%s"/></linearGradient>'
        '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="1.5" r="1.5" fill="%s"/></pattern>'
        '</defs>'
        # plate
        '<rect x="1" y="1" width="998" height="258" rx="22" fill="%s" '
        'stroke="%s" stroke-width="2"/>'
        # dot field, faded out to the right so the text stays clean
        '<rect x="1" y="1" width="998" height="258" rx="22" fill="url(#dots)"/>'
        # accent rule down the left edge
        '<rect x="46" y="58" width="6" height="144" rx="3" fill="url(#g)"/>'
        # name
        '<text x="80" y="120" font-family="%s" font-size="58" font-weight="700" '
        'letter-spacing="1.5" fill="%s" textLength="%s" '
        'lengthAdjust="spacingAndGlyphs">%s</text>'
        # role
        '<text x="82" y="158" font-family="%s" font-size="19" font-weight="500" '
        'fill="%s" textLength="%s" lengthAdjust="spacingAndGlyphs">%s</text>'
        # tag line
        '<text x="82" y="196" font-family="%s" font-size="14" font-weight="500" '
        'letter-spacing="0.6" fill="%s" textLength="%s" '
        'lengthAdjust="spacingAndGlyphs">%s</text>'
        # gradient underline sweeping to the right edge
        '<rect x="1" y="236" width="998" height="5" fill="url(#g)" opacity="0.95"/>'
        '</svg>'
    ) % (ACCENT_A, ACCENT_B, SUCCESS, dot, bg, border,
         FONT, fg, name_w, name,
         FONT, muted, role_w, role,
         MONO, muted, tags_w, tags)


def section(label, icon_hint, dark):
    """A small section header strip, so the page has visual rhythm."""
    fg = TEXT_DARK if dark else TEXT_LIGHT
    border = BORDER_DARK if dark else BORDER_LIGHT
    bg = INK if dark else PAPER
    w = int(text_width(label, 20, 0.8) + 74)
    tw = text_width(label, 20, 0.8)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="48" '
        'viewBox="0 0 %d 48" role="img" aria-label="%s">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient></defs>'
        '<rect x="0.5" y="0.5" width="%d" height="47" rx="10" fill="%s" '
        'stroke="%s" stroke-width="1"/>'
        '<rect x="14" y="13" width="5" height="22" rx="2.5" fill="url(#g)"/>'
        '<text x="30" y="31" font-family="%s" font-size="20" font-weight="650" '
        'letter-spacing="0.8" fill="%s" textLength="%s" '
        'lengthAdjust="spacingAndGlyphs">%s</text>'
        '</svg>'
    ) % (w, w, label, ACCENT_A, ACCENT_B, w - 1, bg, border,
         FONT, fg, tw, label)


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body + "\n")
    print("wrote assets/%s" % name)


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    write("banner.svg", banner(dark=False))
    write("banner-dark.svg", banner(dark=True))
    for label, stem in (("What I build", "s-build"),
                        ("Stack", "s-stack"),
                        ("Activity", "s-activity"),
                        ("Reach me", "s-reach")):
        write(stem + ".svg", section(label, "", dark=False))
        write(stem + "-dark.svg", section(label, "", dark=True))


if __name__ == "__main__":
    main()
