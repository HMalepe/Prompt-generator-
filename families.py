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
 "fiction":    "book craft with continuity guardrails: premise → character bible → world rules → beat outline → chapter drafting that NAMES the craft technique it uses (scene/sequel structure, motivation-reaction units, subtext-in-dialogue, specific sensory detail, consistent POV/tense, anti-cliché) → dialogue → pacing → theme → line edit → blurb. Drafting prompts must direct the AI in HOW to write the scene, not just what happens.",
 "nonfiction": "substance-first: reader avatar → thesis → chapter architecture (idea+proof+application) → drafting that forces real frameworks and flags where author expertise is needed → exercises → intro/outro → title → sales copy.",
 "low_content":"print-ready interior: concept → page taxonomy → exact layout spec (trim, margins, bleed) → repeatable page content → front/back matter → cover concept + KDP metadata (title, subtitle, keywords, categories, description).",
 "marketing":  "direct-response (AIDA/PAS): offer & avatar → voice-of-customer research → big idea → primary asset in full → A/B variations → headline/subject banks → objection handling → CTA optimization → compliance check.",
 "video":      "retention-first: positioning → title & thumbnail banks → hook bank (first 3s) → full script with retention beats → B-roll shotlist → captions → description + tags → repurposing (long→shorts).",
 "visual":     "art direction: visual system (palette, composition, lighting, medium, mood) → base generation string → controlled variations → format/aspect adaptations → typography integration → cleanup/upscale → export spec.",
 "business":   "professional doc: context intake → architecture → section-by-section drafting with specificity → number/KPI/projection logic → red-team review against how a banker/investor/client/auditor reads it → formatting/export.",
 "education":  "pedagogy: objectives → prior-knowledge diagnostic → explanation (concept→analogy→worked example) → practice Qs with answer keys + rationales → spaced-repetition flashcards → misconception targeting → mock assessment. Force fact-verification.",
 "music":      "songwriting: concept & emotional core → title/hook → structure map → section drafting with genre-authentic vocabulary, a disciplined rhyme scheme, syllable-count/stress control, and concrete imagery (no abstractions) → hook sharpening → prosody/singability line-by-line → alt moods → AI-audio tool prompt with genre/BPM/instrumentation spec.",
 "wellness":   "safe general-education plan with real progression logic (sets/reps/RPE or intensity targets, weekly progression, deload structure): intake (goals, constraints, equipment) → foundational education → structured plan → adaptation/substitution → tracking → plateau troubleshooting. MUST stay non-medical, refuse condition-specific medical claims, and append a 'not medical advice — consult a professional' disclaimer.",
 "code_tech":  "ship a working artifact: requirements → architecture plan → scaffold → implement each module (runnable, self-contained code, explicit libs/IO/error handling) → tests → debugging templates → docs → deploy/run.",
}

# ── the premium bar (applied to every generation prompt) ────────────────────
PREMIUM = ("PREMIUM BAR (non-negotiable — this is what people pay real money for):\n"
           "- Encode specific EXPERT methodology the buyer would NOT know to ask for: named "
           "frameworks, industry techniques, concrete parameters and numbers, and the non-obvious "
           "pro moves a novice would skip. The buyer pays for expertise baked into the SEQUENCE, "
           "not for the instruction itself.\n"
           "- BAN filler language: never write 'make it engaging / professional / high-quality / "
           "compelling' without specifying, concretely, exactly what that means and how to do it.\n"
           "- ZERO overlap: each step must introduce a capability, decision, or asset absent from "
           "EVERY prior step — not just the one before it. If step N could merge with an earlier "
           "step, it is filler; replace it with something that materially advances the build.\n"
           "- Each prompt must produce output the buyer could NOT easily get from a one-line "
           "question to the AI. The ordered sequence plus embedded expertise IS the product.")

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
CREATIVE LENS: "{lens}" — use this lens to shape the ANGLE and aesthetic so this batch differs from any other run. The lens flavors the concept only; it must NEVER produce gimmicky, cutesy, or novelty names.

Invent {n} {what}. Names must sound like premium, commercially credible products a serious buyer would pay top dollar for — evocative but professional, never kitschy. No two overlap >20%. Spread mainstream → niche.

Return ONLY a JSON array, no prose, no fences:
[{{"name":"<punchy, premium name>","one_liner":"<max 12 words: who wants it & why>","difficulty":"beginner|intermediate|advanced"}}]
Exactly {n} items."""

# ── prompt generation (chunked) ────────────────────────────────────────────
def prompts(level, *, family, category, subcategory=None, leaf=None,
            outcome, start, count, lens, total=None, prior_steps=None):
    directive = FAMILY[family]
    end = start + count - 1
    arc = ""
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
        # Phase-aware arc so a blind late chunk stops padding and does end-of-build work.
        if total:
            pct = end / total
            if pct <= 0.40:
                arc = (f"\nBUILD PHASE — OPENING (steps {start}–{end} of {total}): lay the strategic and "
                       "structural foundation — decisions, architecture, and setup that every later step depends on.")
            elif pct <= 0.78:
                arc = (f"\nBUILD PHASE — CORE (steps {start}–{end} of {total}): build the main substance section "
                       "by section. Each step produces a concrete, load-bearing part of the deliverable.")
            else:
                arc = (f"\nBUILD PHASE — FINAL (steps {start}–{end} of {total}): the core is ALREADY built. Do NOT "
                       "add more basic/setup sections and do NOT repeat earlier work. These closing prompts must "
                       "deliver advanced technique, differentiation, edge-case handling, polish, conversion/monetization, "
                       "and reusable variations — the material that justifies a premium price. Every one must teach the "
                       "buyer something they could not get from a one-line question to the AI.")
    continuity = ""
    if prior_steps:
        listed = "\n".join(f"  {s}. {g}" for s, g in prior_steps)
        continuity = ("STEPS ALREADY WRITTEN — do NOT repeat, re-introduce, or rebuild any of these. "
                      "Continue the SAME build from where they leave off, in the exact same tech stack, "
                      "file structure, and aesthetic already established above:\n" + listed + "\n\n")
    return f"""You are a top-tier practitioner writing part of a PREMIUM prompt-pack people pay real money for.
FAMILY FOCUS: {directive}
The buyer pastes these prompts, in order, into an AI tool to build {outcome}.
CREATIVE LENS for this batch: "{lens}" — flavor tone and aesthetic only; never let it degrade the professional, premium quality of the instructions.

{PREMIUM}

Write {scope}{arc}
{continuity}Produce build prompts numbered {start}..{start+count-1}, in strict build order, each cumulative (later builds on earlier).
{long}
Where the buyer inserts their own info use [SQUARE_LABELS].

Return ONLY a JSON array, no prose, no fences:
[{{"step":{start},"goal":"<plain goal>","prompt":"<the literal paste-ready prompt>","fill_in":"<[LABELS] or 'nothing'>","expected":"<1 line: what good output looks like>"}}]
Exactly {count} items, steps {start}..{start+count-1}."""
