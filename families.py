"""
families.py — the fuel. Directives per content family + prompt builders for each
of the three tree levels. Placeholders are filled by forge.py.

Tree:  CATEGORY  →  SUBCATEGORY  →  SUB-SUBCATEGORY (leaf)
Prompts live at EVERY level:
  category    : foundational prompts that apply across the whole category
  subcategory : prompts specific to that style/angle
  leaf        : the big 50+ LONG, DETAILED, build-order prompts (the product)
"""

FAMILY = {
 "web_build":  "front-end build: design tokens → layout scaffold → each section → interactivity/animation → responsive → accessibility → performance → copy → deploy. Every prompt states exactly what the AI tool should output (framework, single-file vs components, styling).",
 "fiction":    "book craft with continuity guardrails: premise → character bible → world rules → beat outline → chapter drafting (sensory-specific, anti-cliché, consistent POV/tense) → dialogue → pacing → theme → line edit → blurb.",
 "nonfiction": "substance-first: reader avatar → thesis → chapter architecture (idea+proof+application) → drafting that forces real frameworks and flags where author expertise is needed → exercises → intro/outro → title → sales copy.",
 "low_content":"print-ready interior: concept → page taxonomy → exact layout spec (trim, margins, bleed) → repeatable page content → front/back matter → cover concept + KDP metadata (title, subtitle, keywords, categories, description).",
 "marketing":  "direct-response (AIDA/PAS): offer & avatar → voice-of-customer research → big idea → primary asset in full → A/B variations → headline/subject banks → objection handling → CTA optimization → compliance check.",
 "video":      "retention-first: positioning → title & thumbnail banks → hook bank (first 3s) → full script with retention beats → B-roll shotlist → captions → description + tags → repurposing (long→shorts).",
 "visual":     "art direction: visual system (palette, composition, lighting, medium, mood) → base generation string → controlled variations → format/aspect adaptations → typography integration → cleanup/upscale → export spec.",
 "business":   "professional doc: context intake → architecture → section-by-section drafting with specificity → number/KPI/projection logic → red-team review against how a banker/investor/client/auditor reads it → formatting/export.",
 "education":  "pedagogy: objectives → prior-knowledge diagnostic → explanation (concept→analogy→worked example) → practice Qs with answer keys + rationales → spaced-repetition flashcards → misconception targeting → mock assessment. Force fact-verification.",
 "music":      "songwriting: concept & emotional core → title/hook → structure map → section drafting (genre-authentic rhyme/meter/imagery) → hook sharpening → prosody/singability → alt moods → AI-audio tool prompt.",
 "wellness":   "safe general-education plan with progression logic: intake (goals, constraints) → foundational education → structured plan → adaptation/substitution → tracking → plateau troubleshooting. MUST stay non-medical, refuse condition-specific medical claims, and append a 'not medical advice — consult a professional' disclaimer.",
 "code_tech":  "ship a working artifact: requirements → architecture plan → scaffold → implement each module (runnable, self-contained code, explicit libs/IO/error handling) → tests → debugging templates → docs → deploy/run.",
}

# ── tree expansion ─────────────────────────────────────────────────────────
def expand(kind, *, category, subcategory=None, seed=None, n, lens):
    ctx = f'CATEGORY: "{category}"'
    if subcategory:
        ctx += f'\nSUBCATEGORY: "{subcategory}"'
    what = ("distinct commercial STYLE/ANGLE variants of the category"
            if kind == "sub" else
            "narrower, concrete SUB-VARIANTS of the subcategory (each a specific buildable product angle)")
    seedline = f'\nSEED EXAMPLE: "{seed}"' if seed else ""
    return f"""You are a product architect for a premium prompt-pack catalog.
{ctx}{seedline}
CREATIVE LENS: "{lens}" — let this lens strongly and specifically shape the whole set so this batch differs from any other run. No generic names.

Invent {n} {what}. Vivid, commercially recognizable names. No two overlap >20%. Spread mainstream → niche.

Return ONLY a JSON array, no prose, no fences:
[{{"name":"<punchy name>","one_liner":"<max 12 words: who wants it & why>","difficulty":"beginner|intermediate|advanced"}}]
Exactly {n} items."""

# ── prompt generation (chunked) ────────────────────────────────────────────
def prompts(level, *, family, category, subcategory=None, leaf=None,
            outcome, start, count, lens):
    directive = FAMILY[family]
    if level == "category":
        scope = (f'FOUNDATIONAL prompts for the ENTIRE category "{category}" — reusable '
                 f'setup/strategy/decision prompts a builder needs before choosing a specific style.')
        long = "Each prompt medium length, reusable, and self-contained."
    elif level == "subcategory":
        scope = (f'prompts specific to the "{subcategory}" style within "{category}".')
        long = "Each prompt concrete and self-contained."
    else:
        scope = (f'the core build prompts for the specific product "{leaf}" '
                 f'({subcategory} → {category}). This is the paid deliverable.')
        long = ("Each prompt must be LONG and DETAILED (aim 120–250 words): full context, "
                "explicit constraints, tone, format, and an explicit 'output only X' instruction. "
                "Written so it works pasted cold into a fresh AI chat.")
    return f"""You are a senior practitioner writing part of a premium prompt-pack.
FAMILY FOCUS: {directive}
The buyer pastes these prompts, in order, into an AI tool to build {outcome}.
CREATIVE LENS for this batch: "{lens}".

Write {scope}
Produce build prompts numbered {start}..{start+count-1}, in strict build order, each cumulative (later builds on earlier).
{long}
Where the buyer inserts their own info use [SQUARE_LABELS].

Return ONLY a JSON array, no prose, no fences:
[{{"step":{start},"goal":"<plain goal>","prompt":"<the literal paste-ready prompt>","fill_in":"<[LABELS] or 'nothing'>","expected":"<1 line: what good output looks like>"}}]
Exactly {count} items, steps {start}..{start+count-1}."""
