# sovernti-og — OG Wrapper Hosting (Cloudflare Pages)

> Static-only host for Sovernti's OG wrapper pages. Serves per-clip Open Graph + Twitter Card metadata that LinkedIn / Facebook / Slack / iMessage scrape to render inline-playable video previews.
>
> **Live at:** `https://og.sovernti.com/svn-sNN.html` (where NN = 01-09)
> **Hosted on:** Cloudflare Pages (free tier)
> **GitHub repo:** `tolga-bit/sovernti-og` (public)
> **Created:** 8 May 2026 (Day 102, Session 60 part A continuation)

---

## Why this exists

Sovernti's main app is hosted on Lovable. Lovable's serve-time runtime (SPA build pipeline + analytics injection + SEO normalization) was overriding our static OG wrapper pages — stripping twitter:player tags, injecting wrong twitter:image, and modifying meta refresh to instant redirect that caused LinkedIn's crawler to follow to the homepage. After two failed Lovable-side fixes, the wrappers were migrated to Cloudflare Pages — a static-only host that serves files byte-for-byte as committed.

Trigger: SVN-S08 inaugural LinkedIn post (Session 59 part D, 8 May 2026 afternoon) rendered as generic Sovernti site card instead of per-clip preview. See `04-Decisions/2026-05-08-OG-Wrappers-Cloudflare-Pages-Migration.md`.

---

## Files in this directory

| File | Purpose |
|---|---|
| `wrapper.template.html` | The canonical wrapper template with `{{SLUG}}` / `{{TITLE}}` / `{{DESCRIPTION}}` / `{{IMAGE_ALT}}` / `{{VIDEO_FILENAME}}` placeholders |
| `build.py` | Generates the 9 wrapper HTMLs from the template + per-clip metadata array |
| `svn-s01.html` ... `svn-s09.html` | The 9 per-clip wrapper pages (auto-generated — DO NOT edit by hand; edit `build.py` instead) |
| `deploy.sh` | One-command deploy script: rebuild + git add + commit + push |
| `Future-Option-F-Manifest-Driven-Build-Spec.md` | Future-state spec for upgrading to manifest-driven generation via GitHub Actions (when scale justifies it) |
| `README.md` | This file |

---

## Adding a new clip (current workflow — Option A)

**~30 seconds per new clip.**

1. Open `build.py`, append a new dict to the `CLIPS` list with the 5 fields:
   ```python
   {
       "slug": "svn-s10",
       "video_filename": "SVN-S10-new-clip-8s.mp4",
       "title": "Your wine, breathing at the table before you arrive.",
       "description": "Sovernti — managed custody for collectors who already know what they want to drink. Cultivating our founding-member cohort across London now.",
       "image_alt": "Brief alt-text describing the clip.",
   },
   ```
2. Confirm the matching `.mp4` and `posters/svn-s10.jpg` are uploaded to Supabase social-clips bucket (use the `social-clips-upload` edge fn or Supabase Dashboard).
3. Run `./deploy.sh "Add SVN-S10"` — rebuilds all wrappers, commits, pushes.
4. Cloudflare Pages auto-deploys. Live at `https://og.sovernti.com/svn-s10.html` in ~30-60 seconds.

That's it.

---

## Pre-publish verification protocol

Before flipping any Deployment Ledger row to VERIFIED for a new wrapper, follow `99-System/templates/Verification-Evidence-Standard.md`:

1. **Structural curl:**
   ```bash
   curl -sL https://og.sovernti.com/svn-sNN.html | grep -c og:video
   ```
   Expect `5`.

2. **Crawler-UA curl:**
   ```bash
   curl -sL -A "LinkedInBot/1.0" https://og.sovernti.com/svn-sNN.html | grep og:title
   ```
   Expect per-clip og:title.

3. **LinkedIn Post Inspector (sufficient — IS the evidence):**
   - Paste `https://og.sovernti.com/svn-sNN.html` into `https://www.linkedin.com/post-inspector/`
   - Confirm preview shows per-clip poster + per-clip og:title (NOT generic Sovernti site card)
   - Capture screenshot — this is the artefact for the Ledger row evidence column

4. **Twitter Card Validator (if posting to X):**
   - `https://cards-dev.twitter.com/validator`
   - Confirm `player` card type renders with per-clip image

---

## Cloudflare Pages setup (one-time, already done)

Documented for the record. Re-run only if migrating to a new CF account or rebuilding the project.

1. **Create GitHub repo:** `tolga-bit/sovernti-og` (public).
2. **Initial commit:** push the contents of this directory (excluding `README.md` if you don't want it in the public repo — but probably fine to include).
3. **Cloudflare Pages → Create Project → Connect to Git** → select `tolga-bit/sovernti-og`.
4. **Build settings:** leave blank — pure static, no build command.
5. **Production branch:** `main`.
6. **Custom Domain:** add `og.sovernti.com`. Cloudflare auto-creates the CNAME (DNS already on Cloudflare). SSL provisions in ~2-5 min.
7. **Verify:** visit `https://og.sovernti.com/svn-s08.html` in browser — should show video preview + redirect to sovernti.com after 2s. View Source — should match the file in this directory exactly.

---

## When to upgrade to Option F (manifest-driven build via GitHub Actions)

Current Option A workflow (edit `build.py`, run `deploy.sh`) is sufficient for ~1-3 wrapper additions per week.

**Trigger to upgrade to Option F:**
- 20+ wrappers in production (clips * languages * variants)
- Per-restaurant pages added (1 per partner, scaling to 20+)
- Per-event / per-campaign pages added regularly
- Want to delegate adding wrappers to a non-engineer

Option F architecture: clips defined in `clips.json`, GitHub Action runs `build.py` on every push, deploys generated wrappers to Cloudflare Pages. Adding a wrapper becomes "edit JSON, push" — no Python knowledge required.

Full spec: `Future-Option-F-Manifest-Driven-Build-Spec.md` in this directory.

---

## Cross-references

- `04-Decisions/2026-05-08-OG-Wrappers-Cloudflare-Pages-Migration.md` — decision record + reasoning
- `99-System/templates/Verification-Evidence-Standard.md` — pre-VERIFIED evidence requirements
- `Sovernti-Vault/.claude/skills/social-deploy/SKILL.md` v1.6+ — deployment skill, references this directory's wrapper URLs
- `05-Build/Deployment-Ledger.md` row 153 — current state of OG wrapper deployment
- `08-Brand/Social-Clips/9x16/` — the source 9:16 clips this directory wraps
- `99-System/scripts/upload-social-clip.sh` — Supabase upload script for new clips

---

*Initial scaffolding 8 May 2026 (Day 102, Session 60 part A continuation). Maintained as the canonical source of OG wrapper hosting.*
