# CLAUDE.md — Prompt Forge

Project memory for Claude Code. Read this fully at the start of every session.

## What this is
An internal content-production tool. One command forges a fresh tree of AI prompts
and writes it to a new **dated build**. Old builds are never overwritten. Leaves are
sellable products: 50+ long, detailed, copy-paste prompts. Any leaf exports to a
polished Word + PDF to sell.

## Golden rule
**The architecture is built and tested. Do NOT rewrite or "refactor" it.** Help run,
extend, debug, and export — not redesign. If you think something needs restructuring,
explain why and wait for my explicit yes before changing structure. Small bug fixes are
fine; announce them.

## The tree (prompts at every level)
```
library/builds/<TIMESTAMP>/
  <category>/
    _category.json            ~12 foundational prompts for the whole category
    <subcategory>/
      _subcategory.json       ~24 prompts for that style/angle
      <sub-subcategory>.json  50+ LONG build prompts  ← the product
  manifest.json               tree + total prompt count
library/LATEST.txt            points at newest build
```

## Files (what each does — don't move logic between them)
- `forge.py`      — engine + CLI: tree build, chunked prompt generation, dated
                    versioning, resume (checkpoint per build), mock mode.
- `families.py`   — the "fuel": per-family directives + the three-level prompt
                    builders. **This is where prompt QUALITY lives.** Tune wording
                    here to improve output; don't touch the engine to do it.
- `seeds.json`    — level-1 categories. Add rows here to scale toward 102.
- `export_docx.py`— leaf JSON → styled Word (.docx) → PDF (via LibreOffice).

## Commands
```bash
# free dry-run — no API key, mock content, proves the pipeline
python forge.py build --category websites --dry-run

# real content (needs the key set)
export ANTHROPIC_API_KEY=sk-ant-...
python forge.py build --category websites          # one category tree
python forge.py build --all                        # every category (costly)

python forge.py list                               # dated builds + counts
python forge.py list-categories                    # seed categories

# export a product
python export_docx.py --json library/builds/<STAMP>/<cat>/<sub>/<leaf>.json
python export_docx.py --json <leaf.json> --no-pdf  # Word only
```

Tuning flags on `build`: `--subs --subsubs --leaf-prompts --sub-prompts
--cat-prompts --chunk --concurrency --max-tokens --model`.

## Cost reality — respect it before any real run
Real content = real API calls. ~50 leaf prompts ÷ chunk(10) = 5 calls per leaf.
Default fan-out (8 subs × 5 subsubs = 40 leaves) ≈ a few hundred calls per category:
minutes and real dollars. `--all` across 100+ categories is thousands of calls.
Before running anything LIVE that isn't a single category, tell me the estimated
call count and get my confirmation. Builds resume on interruption, so never re-run a
completed build "to be safe" — that just spends twice.

## Conventions
- Python 3.10+, run inside `.venv`. Model default: `claude-sonnet-4-6`.
- Prefer editing `families.py` to change prompt quality; `seeds.json` to add scope.
- Never delete anything under `library/builds/` — that's the versioned archive.
- Keep the tool single-language (Python + pip). Don't add a Node dependency.
- PDF export needs `soffice` (LibreOffice) on PATH.

## When I ask to "improve the prompts"
Edit the directives/builders in `families.py`, run a `--dry-run` to confirm the
pipeline still parses, then a small LIVE test (`--subs 1 --subsubs 1 --leaf-prompts 6`)
on one category so I can judge quality cheaply before a full build.
