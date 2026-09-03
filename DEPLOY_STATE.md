# DEPLOY_STATE

**Canonical production URL:** https://t3dy.github.io/BRUNOMEMAPP/
**Repository:** https://github.com/t3dy/BRUNOMEMAPP (public)

## What serves what

| | |
|---|---|
| **Host** | GitHub Pages |
| **Source** | branch `gh-pages`, path `/` |
| **Content** | the built contents of `site/` from `master` |
| **Build** | none on the server — the site is pre-built and committed |

There is only one host. No Vercel, no second config. If that changes, record it here first.

## How to deploy a change

```bash
python scripts/seed_from_json.py     # if seed JSON changed
python scripts/build_site.py         # regenerate site/
git add -A && git commit -m "..."
git push origin master
git subtree push --prefix site origin gh-pages   # publishes
```

`git subtree push` is the publish step. Pushing `master` alone changes nothing on the live site.

## Env vars / secrets

None. The site is fully static: no API keys, no backend, no runtime configuration.

## Gotchas

- **`docs/` is not the Pages source.** It holds the design documents. Pages serves `gh-pages`, not `/docs`. Do not switch the Pages source to `/docs` — it would publish the design record instead of the site.
- **`site/style.css` and `site/*.js` are hand-maintained**, not generated. `build_site.py` writes HTML only and will not overwrite them.
- **The database is gitignored.** A fresh clone must run `init_db.py` then `seed_from_json.py` before `build_site.py`.
- **The corpus is not in the repository** and is not redistributable. The harvest scripts read `E:\pdf\renaissance magic\Bruno Lull\plain_text_drafts\`; their output JSON *is* committed, so the site builds without the corpus present.
- **`git subtree push` rewrites history for `gh-pages`.** If it ever rejects, `git push origin $(git subtree split --prefix site master):gh-pages --force`.

## Verified live (2026-09-02)

- All routes 200: `/`, `/engine.html`, `/fantastica.html`, `/designs.html`, `/practices/index.html`, `/images/courts.html`, `/design-engine.html`, plus `style.css`, `engine.js`, `fantastica.js`.
- **The Art Engine** played end to end against the live URL: `E → I → R → E`, "Demonstratio completa".
- **Logica Fantastica** played end to end against the live URL: `E → I → R → E`, "Demonstratio per imagines".
- CSS applied, embedded JSON data present in both instruments.
