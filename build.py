#!/usr/bin/env python3
"""
build.py — Generate 9 OG wrapper HTML files from the template + per-clip metadata.

Usage:
  python3 build.py

Output: writes svn-s01.html through svn-s09.html alongside this script.

For Option F (future): replace the inline CLIPS list with a clips.json read,
make the script idempotent, and have a GitHub Action call this on every push.

Spec: 99-System/sovernti-og/Future-Option-F-Manifest-Driven-Build-Spec.md
"""

from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE_PATH = HERE / "wrapper.template.html"

# The 9 social clips. Edit this list to add a new clip in the simplest possible form.
# (For the manifest-driven Option F upgrade, this list moves into a `clips.json` file
# that's read by the GitHub Action — the schema is the same fields below.)
CLIPS = [
    {
        "slug": "svn-s01",
        "video_filename": "SVN-S01-warehouse-pan-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Sovernti bonded warehouse — where your wine sleeps.",
    },
    {
        "slug": "svn-s02",
        "video_filename": "SVN-S02-label-CU-and-OL1-card-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "A wine label in macro — Sovernti's editorial provocation: your wine deserves better than this.",
    },
    {
        "slug": "svn-s03",
        "video_filename": "SVN-S03-decanting-golden-hour-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Wine being decanted in golden hour, 90 minutes before service.",
    },
    {
        "slug": "svn-s04",
        "video_filename": "SVN-S04-greeting-red-bus-arrival-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Couple arriving at a London restaurant, red double-decker passing the entrance.",
    },
    {
        "slug": "svn-s05",
        "video_filename": "SVN-S05-hero-couple-sommelier-pour-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Sommelier pouring wine for a couple — the briefing card on the table.",
    },
    {
        "slug": "svn-s06",
        "video_filename": "SVN-S06-QR-blockchain-UI-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Sovernti chain of custody — every bottle, every step, verified on blockchain.",
    },
    {
        "slug": "svn-s07",
        "video_filename": "SVN-S07-coravin-margaux-decanter-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Coravin pour through a Premier Cru — Proof Reserve Protocol in action.",
    },
    {
        "slug": "svn-s08",
        "video_filename": "SVN-S08-final-table-golden-hour-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "An empty restaurant table at golden hour, set for the evening — your wine, breathing at the table before you arrive.",
    },
    {
        "slug": "svn-s09",
        "video_filename": "SVN-S09-closing-seal-tagline-URL-8s.mp4",
        "title": "Your wine, breathing at the table before you arrive.",
        "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
        "image_alt": "Sovernti wax seal end card — your wine, breathing at the table before you arrive.",
    },
]


def build_all() -> None:
    template = TEMPLATE_PATH.read_text()
    written = []
    for clip in CLIPS:
        html = (
            template
            .replace("{{SLUG}}", clip["slug"])
            .replace("{{VIDEO_FILENAME}}", clip["video_filename"])
            .replace("{{TITLE}}", clip["title"])
            .replace("{{DESCRIPTION}}", clip["description"])
            .replace("{{IMAGE_ALT}}", clip["image_alt"])
        )
        out = HERE / f"{clip['slug']}.html"
        out.write_text(html)
        written.append(out.name)
    print(f"Built {len(written)} wrapper(s):")
    for name in written:
        print(f"  - {name}")


if __name__ == "__main__":
    build_all()
