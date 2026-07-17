# Prompt Forge — production engine

Your internal content-production tool. One command forges a fresh tree of prompts
and writes it to a new **dated build**. Old builds are never overwritten — every
version you ever forge is kept, dated. Then export any leaf to a sellable Word/PDF.

## The tree (prompts at every level)

```
library/builds/<TIMESTAMP>/
  <category>/
    _category.json                 12 foundational prompts for the whole category
    <subcategory>/
      _subcategory.json            24 prompts for that style/angle
      <sub-subcategory>.json       premium zero-filler build prompts (count per family)  ← the product
  manifest.json                    tree + total prompt count
library/LATEST.txt                 points at newest build
```

## One button = one build

```bash
# free full dry-run (mock content, proves the whole pipeline, no key/spend)
python forge.py build --category websites --dry-run

# real content (set your key first)
export ANTHROPIC_API_KEY=sk-ant-...
python forge.py build --category websites          # one category's whole tree
python forge.py build --all                        # every category (costly — scope on purpose)

python forge.py list                               # every dated build + counts
python forge.py list-categories                    # the seed categories
```

At default fan-out (`--subs 8 --subsubs 5`) with per-family leaf counts (~28 for websites)
one category build is ~40 leaves × ~28 + sub/category prompts ≈ **~1,300 prompts per press**. Old builds stay,
so you get a dated version history automatically.

Tune per run: `--subs --subsubs --leaf-prompts --sub-prompts --cat-prompts
--chunk --concurrency --max-tokens --model`.

## Export a sellable document

```bash
python export_docx.py --json library/builds/<STAMP>/websites/<sub>/<leaf>.json
# -> <leaf>.docx  and  <leaf>.pdf  next to the json
python export_docx.py --json <leaf.json> --no-pdf   # Word only
```

Word is the source of truth; the PDF is rendered from it (identical layout) via
LibreOffice. The layout: category eyebrow, title, one-liner, how-to, then every
prompt as a numbered STEP with a shaded "PASTE THIS" box, Fill-in and Expected lines.

## Reality check on cost/scale

Real content = real API calls: ~28 leaf prompts ÷ chunk(10) ≈ 3 calls per leaf, so a
default category build is a few hundred calls — minutes and real dollars, not seconds.
`--all` across 100+ categories is thousands of calls; run it deliberately, ideally one
category at a time. The build resumes if interrupted (checkpoint per build), so nothing
is repaid. There is zero benefit to regenerating a build you already have — that's why
each press makes a *new* dated one and leaves the rest alone.

## Scaling to 102 categories

Add rows to `seeds.json` (id, family, outcome, seed). `family` ∈
web_build, fiction, nonfiction, low_content, marketing, video, visual, business,
education, music, wellness, code_tech. No code changes.

## Files
- `forge.py` — engine + CLI (tree, chunking, versioning, resume, mock mode)
- `families.py` — family directives + the three-level prompt builders (the fuel)
- `seeds.json` — level-1 categories
- `export_docx.py` — leaf → sellable Word + PDF
