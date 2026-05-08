# Option F — Manifest-Driven Build Spec (Future Upgrade)

> **Status:** SPEC — not implemented. Activate when scale justifies (~20+ wrappers, or per-restaurant pages, or non-engineer adding wrappers).
> **Authored:** 8 May 2026 (Day 102, Session 60 part A continuation)
> **Builds on:** Option A (current) — Cloudflare Pages + GitHub repo `tolga-bit/sovernti-og`
> **Effort to implement:** ~2-3 hours one-time, fully reversible
> **Decision record:** `04-Decisions/2026-05-08-OG-Wrappers-Cloudflare-Pages-Migration.md`

---

## Why this exists

Option A (current state) ships clean static wrappers with a Python build script. Per-clip metadata lives in a `CLIPS` list inside `build.py`. Adding a clip = edit Python list + run `deploy.sh`.

Option F upgrades this to manifest-driven generation:
- Per-clip metadata lives in `clips.json` (not Python)
- A GitHub Action runs `build.py` automatically on every push
- Adding a clip = edit JSON + push (no Python knowledge required)
- The build artefact is committed back to `main` OR built fresh by Cloudflare Pages

**When to activate:**
- 20+ wrappers in production (clip × language × variant matrix)
- Per-restaurant wrapper pages (1 per partner, scaling to 20+)
- Per-event / per-campaign pages added regularly
- Want to delegate wrapper creation to a non-engineer (community manager, marketing assistant, etc.)

**When NOT to activate:**
- Current scale (≤9 wrappers) — Option A is faster and simpler
- Wrapper schema changes frequently — JSON manifest adds friction when iterating on the template
- No need for non-engineer authoring — Option A is fine

---

## Architecture

```
GitHub repo `tolga-bit/sovernti-og`
├── clips.json                         ← Manifest (edit this to add clips)
├── wrapper.template.html              ← Template (rarely edited)
├── build.py                           ← Reads clips.json, writes svn-sNN.html files
├── .github/workflows/build.yml        ← GitHub Action: runs build.py on push, commits results
├── svn-s01.html ... svn-sNN.html      ← Auto-generated, committed
├── deploy.sh                          ← Manual escape hatch
└── README.md
```

### How `clips.json` looks

```json
{
  "clips": [
    {
      "slug": "svn-s01",
      "video_filename": "SVN-S01-warehouse-pan-8s.mp4",
      "title": "Your wine, breathing at the table before you arrive.",
      "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
      "image_alt": "Sovernti bonded warehouse — where your wine sleeps."
    },
    {
      "slug": "svn-s02",
      "video_filename": "SVN-S02-label-CU-and-OL1-card-8s.mp4",
      "title": "...",
      "description": "...",
      "image_alt": "..."
    }
  ]
}
```

### How `.github/workflows/build.yml` looks

```yaml
name: Build OG Wrappers

on:
  push:
    branches: [main]
    paths:
      - 'clips.json'
      - 'wrapper.template.html'
      - 'build.py'
      - '.github/workflows/build.yml'

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run build
        run: python3 build.py

      - name: Commit generated wrappers
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add svn-s*.html
          if git diff --staged --quiet; then
            echo "No wrapper changes — skipping commit."
          else
            git commit -m "auto: rebuild wrappers from clips.json [skip ci]"
            git push
          fi
```

### How `build.py` changes for Option F

Replace the inline `CLIPS` list with a JSON read:

```python
import json
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE_PATH = HERE / "wrapper.template.html"
MANIFEST_PATH = HERE / "clips.json"

def build_all() -> None:
    template = TEMPLATE_PATH.read_text()
    manifest = json.loads(MANIFEST_PATH.read_text())
    written = []
    for clip in manifest["clips"]:
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
```

Backwards-compatible: existing wrapper output is byte-for-byte identical.

---

## Migration steps (Option A → Option F)

**Total effort: ~2-3 hours.**

### Step 1 — Extract manifest from build.py (15 min)

```bash
cd 99-System/sovernti-og  # OR cd <local-clone-of-sovernti-og>

# Manually convert the Python CLIPS list to clips.json
# (Or write a one-shot extraction script — Option F's build.py has the same shape)
```

Save as `clips.json` per the schema above.

### Step 2 — Update build.py to read clips.json (20 min)

Replace the inline `CLIPS` list with the JSON read shown above. Verify rebuild produces byte-identical output:

```bash
diff <(python3 build.py && cat svn-s08.html) <(git show HEAD:svn-s08.html)
# Expect: empty diff
```

### Step 3 — Add GitHub Action (30 min)

Create `.github/workflows/build.yml` with the YAML above. Test by:
1. Editing `clips.json` to add a stub new clip (or just touch a comment in build.py)
2. Push to a feature branch → confirm Action runs and commits generated wrappers
3. Merge to main

### Step 4 — Update README + decision record (30 min)

- README: change "Adding a new clip" section to point at clips.json instead of build.py
- README: change deploy.sh usage note (deploy.sh becomes optional — `git push clips.json` is enough)
- Decision record: update `04-Decisions/2026-05-08-OG-Wrappers-Cloudflare-Pages-Migration.md` with Option F activation note + date

### Step 5 — Soak test (30 min)

- Add a real new wrapper via clips.json edit + push only
- Confirm Cloudflare Pages deploys
- Confirm Post Inspector shows correct preview
- Capture as evidence for Verification Evidence Standard

### Step 6 — Update social-deploy SKILL (15 min)

Bump SKILL version (e.g., v1.6 → v1.7). Update the "When to use this skill" section to mention "edit clips.json" instead of "edit build.py" for adding wrappers.

### Step 7 — Optional: lock build.py read access (10 min)

If non-engineers will edit clips.json: protect build.py via CODEOWNERS or a branch protection rule so they can't accidentally break the build script.

---

## What this DOES NOT change

- Cloudflare Pages config (still serves static files from main branch)
- DNS / SSL setup (still og.sovernti.com)
- Wrapper output URL pattern (still `/svn-sNN.html`)
- Per-clip metadata schema (still 5 fields)
- Verification protocol (still Post Inspector + curl per Standard)
- Any vault-side artefacts outside this directory

Pure local upgrade to the build pipeline.

---

## Future Option G — beyond Option F

If/when the manifest-driven build itself feels limiting, the next upgrade path is:

**Option G — Supabase-driven build:**

- Wrappers regenerated automatically when a new row appears in a `social_clips` Supabase table
- Schema: `id`, `slug`, `video_filename`, `title`, `description`, `image_alt`, `published_at`
- A Supabase webhook → GitHub repository_dispatch → triggers Action that pulls the manifest from Supabase API and rebuilds
- Adding a wrapper becomes: insert a row in Supabase + upload the .mp4 + upload the poster
- Could be triggered from an admin UI or from the existing `social-clips-upload` edge fn flow

**When to activate Option G:**
- Wrapper count exceeds ~50 (clips.json gets unwieldy)
- Wrappers need to be created from a non-developer admin UI
- Per-restaurant pages are dynamic (pulled from `restaurants` table)
- Per-event pages tied to live experiences in the platform DB

Option G is significant engineering (~6-8 hours) and only worth it at meaningful scale.

For now, Option F is the next stop. Option G is the horizon.

---

## Cross-references

- `99-System/sovernti-og/README.md` — current Option A operating docs
- `04-Decisions/2026-05-08-OG-Wrappers-Cloudflare-Pages-Migration.md` — decision record
- `99-System/templates/Verification-Evidence-Standard.md` — pre-VERIFIED requirements (apply to every wrapper deploy)
- `Sovernti-Vault/.claude/skills/social-deploy/SKILL.md` v1.6+ — deployment skill (will reference this directory in v1.6, will reference clips.json schema in v1.7+ post-Option F)

---

*Spec v1.0 — 8 May 2026. Activate the upgrade with the migration steps above when the trigger conditions hit. Until then, Option A in `build.py` stays canonical.*
