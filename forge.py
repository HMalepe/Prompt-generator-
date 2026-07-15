#!/usr/bin/env python3
"""
forge.py — the production engine.

ONE BUTTON = one build. Each build regenerates a fresh tree of prompts and writes
it to a NEW dated folder. Old builds are never overwritten — they stay, dated, so
you keep every version you ever forged.

Tree (prompts at every level):
  library/builds/<TIMESTAMP>/<category>/
      _category.json                      <- foundational category prompts
      <subcategory>/
          _subcategory.json               <- style-specific prompts
          <sub-subcategory>.json          <- the 50+ LONG build prompts (the product)
  library/builds/<TIMESTAMP>/manifest.json
  library/LATEST.txt                      <- points at newest build

Scope of one click:
  build --category websites   -> one category's whole tree = thousands of prompts
  build --all                 -> every category (long + costly; scope deliberately)

CLI
  python forge.py build --category websites            # real (needs ANTHROPIC_API_KEY)
  python forge.py build --category websites --dry-run  # free mock, full pipeline
  python forge.py build --all --dry-run
  python forge.py list                                 # every dated build + counts
  python forge.py --help

Resilience: resumes within a build (checkpoint), exponential backoff, capped
concurrency, mock mode when no key.
"""
import os, re, json, argparse, asyncio, hashlib
from pathlib import Path
from datetime import datetime, timezone

import families as F

try:
    from anthropic import AsyncAnthropic
    _SDK = True
except Exception:
    _SDK = False

ROOT = Path(__file__).parent
LIB = ROOT / "library"
BUILDS = LIB / "builds"
LENSES = ["Neon Bazaar","Quiet Brutalism","Analog Warmth","Hyper-Editorial","Cosmic Folk",
          "Vaporwave Luxe","Off-World Minimal","Maximal Baroque","Underground Zine","Soft Utopian",
          "Retro-Terminal","Molten Industrial","Botanical Grid","Midnight Playful","Concrete Poetry",
          "Feral Elegance","Sunbaked Pastel","Chrome Gothic"]

import random
def lens(): return random.choice(LENSES)
def slug(s): return re.sub(r"[^a-z0-9]+","-",str(s).lower()).strip("-")[:60]
def now(): return datetime.now().strftime("%H:%M:%S")

# ── model client (real or mock) ────────────────────────────────────────────
class Client:
    def __init__(self, model, mock):
        self.model = model
        self.mock = mock or not _SDK or not os.getenv("ANTHROPIC_API_KEY")
        self._c = None if self.mock else AsyncAnthropic()
    async def complete(self, prompt, max_tokens):
        if self.mock:
            return _mock(prompt)
        m = await self._c.messages.create(model=self.model, max_tokens=max_tokens,
                                           messages=[{"role":"user","content":prompt}])
        return "".join(b.text for b in m.content if getattr(b,"type","")=="text")

def _mock(prompt):
    if "distinct" in prompt or "SUB-VARIANTS" in prompt:
        n = int(re.search(r"Exactly (\d+) items", prompt).group(1))
        return json.dumps([{"name":f"Mock Variant {i+1}","one_liner":"a distinct angle buyers choose",
                            "difficulty":"beginner"} for i in range(n)])
    m = re.search(r"steps (\d+)\.\.(\d+)", prompt)
    a,b = (int(m.group(1)), int(m.group(2))) if m else (1,6)
    return json.dumps([{"step":i,"goal":f"mock step {i}",
                        "prompt":f"MOCK long prompt {i}. "*20,
                        "fill_in":"nothing","expected":"a usable result"} for i in range(a,b+1)])

async def backoff(fn, tries=6, base=2.0):
    for k in range(tries):
        try: return await fn()
        except Exception as e:
            if k==tries-1: raise
            w = base**k
            if any(x in str(e).lower() for x in ("rate","overloaded","429","529")): w*=2
            await asyncio.sleep(w)

def parse_arr(txt):
    t = txt.strip().replace("```json","").replace("```","").strip()
    s,e = t.find("["), t.rfind("]")
    if s!=-1 and e!=-1:
        try: return json.loads(t[s:e+1])
        except: pass
    out=[]
    for o in re.findall(r"\{[^{}]*\}", t):
        try: out.append(json.loads(o))
        except: pass
    return out

# ── chunked prompt generation to reach a target count ──────────────────────
async def gen_prompts(client, cfg, *, level, family, category, outcome,
                      subcategory=None, leaf=None, target, chunk, mx):
    items, start = [], 1
    while len(items) < target:
        n = min(chunk, target-len(items))
        p = F.prompts(level, family=family, category=category, subcategory=subcategory,
                      leaf=leaf, outcome=outcome, start=start, count=n, lens=lens(), total=target)
        raw = await backoff(lambda: client.complete(p, max_tokens=mx))
        got = [x for x in parse_arr(raw) if x.get("prompt")]
        if not got: break
        # renumber defensively so steps are contiguous
        for i,x in enumerate(got): x["step"] = start+i
        items += got
        start += len(got)
    return items[:target] if len(items)>=target else items

# ── build one category tree ────────────────────────────────────────────────
async def build_category(client, cfg, cat, build_dir, sem, ck, progress):
    fam, outcome = cat["family"], cat["outcome"]
    cdir = build_dir / cat["id"]; cdir.mkdir(parents=True, exist_ok=True)

    async def guarded(coro):
        async with sem: return await coro

    # 1) category-level foundational prompts
    if _pending(ck, "cat", cat["id"]):
        cprompts = await guarded(gen_prompts(client, cfg, level="category", family=fam,
                        category=cat["id"], outcome=outcome,
                        target=cfg["cat_prompts"], chunk=cfg["chunk"], mx=cfg["mx"]))
        _write(cdir/"_category.json", {"category":cat["id"],"family":fam,"prompts":cprompts})
        _done(ck,"cat",cat["id"]); progress(len(cprompts))

    # 2) subcategories
    subs = await guarded(_expand(client, "sub", category=cat["id"], seed=cat.get("seed"),
                                 n=cfg["subs"]))
    for sub in subs:
        sname = sub["name"]; sdir = cdir/slug(sname); sdir.mkdir(exist_ok=True)
        if _pending(ck,"sub",cat["id"],sname):
            sp = await guarded(gen_prompts(client, cfg, level="subcategory", family=fam,
                        category=cat["id"], subcategory=sname, outcome=outcome,
                        target=cfg["sub_prompts"], chunk=cfg["chunk"], mx=cfg["mx"]))
            _write(sdir/"_subcategory.json",
                   {"category":cat["id"],"subcategory":sname,"one_liner":sub.get("one_liner",""),"prompts":sp})
            _done(ck,"sub",cat["id"],sname); progress(len(sp))

        # 3) sub-subcategories (leaves) — the 50+ long prompts
        subsubs = await guarded(_expand(client,"subsub",category=cat["id"],
                        subcategory=sname, n=cfg["subsubs"]))
        for leaf in subsubs:
            lname = leaf["name"]
            if not _pending(ck,"leaf",cat["id"],sname,lname): continue
            lp = await guarded(gen_prompts(client, cfg, level="leaf", family=fam,
                        category=cat["id"], subcategory=sname, leaf=lname, outcome=outcome,
                        target=cfg["leaf_prompts"], chunk=cfg["chunk"], mx=cfg["mx"]))
            _write(sdir/f"{slug(lname)}.json",
                   {"category":cat["id"],"subcategory":sname,"leaf":lname,
                    "one_liner":leaf.get("one_liner",""),"difficulty":leaf.get("difficulty",""),
                    "prompt_count":len(lp),"prompts":lp})
            _done(ck,"leaf",cat["id"],sname,lname); progress(len(lp))
    return subs

async def _expand(client, kind, **kw):
    cache_key = "cache_" + hashlib.sha1(json.dumps({**kw,"k":kind},default=str).encode()).hexdigest()[:12]
    p = F.expand(kind, lens=lens(),
                 category=kw.get("category"), subcategory=kw.get("subcategory"),
                 seed=kw.get("seed"), n=kw["n"])
    raw = await backoff(lambda: client.complete(p, max_tokens=1500))
    arr = [x for x in parse_arr(raw) if x.get("name")]
    return arr or [{"name":f"{kw.get('subcategory') or kw.get('category')} {i+1}"} for i in range(kw["n"])]

# ── checkpoint helpers ─────────────────────────────────────────────────────
def _key(*p): return hashlib.sha1("::".join(map(str,p)).encode()).hexdigest()[:16]
def _pending(ck,*p): return _key(*p) not in ck["done"]
def _done(ck,*p): ck["done"][_key(*p)]=True
def _write(path, obj): path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))

# ── orchestration ──────────────────────────────────────────────────────────
async def run(cfg):
    seeds = json.loads((ROOT/"seeds.json").read_text())["categories"]
    if cfg["category"]:
        seeds = [c for c in seeds if c["id"]==cfg["category"]]
        if not seeds: raise SystemExit(f"Unknown category '{cfg['category']}'. Run: python forge.py list-categories")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    build_dir = BUILDS/stamp; build_dir.mkdir(parents=True, exist_ok=True)
    ckfile = build_dir/"_checkpoint.json"
    ck = json.loads(ckfile.read_text()) if ckfile.exists() else {"done":{}}
    client = Client(cfg["model"], cfg["mock"])
    sem = asyncio.Semaphore(cfg["concurrency"])

    total_prompts = [0]
    def progress(n):
        total_prompts[0]+=n
        if total_prompts[0] % 200 < n:
            _write(ckfile, ck)
            print(f"  [{now()}] {total_prompts[0]} prompts forged...")

    print(f"[{now()}] BUILD {stamp}  mode={'MOCK' if client.mock else 'LIVE'}  "
          f"categories={len(seeds)}  fan-out={cfg['subs']}x{cfg['subsubs']}  leaf={cfg['leaf_prompts']}")
    tree = {}
    for cat in seeds:
        print(f"[{now()}] forging category: {cat['id']}")
        subs = await build_category(client, cfg, cat, build_dir, sem, ck, progress)
        _write(ckfile, ck)
        tree[cat["id"]] = [s["name"] for s in subs]

    manifest = {"build":stamp,"generated":datetime.now(timezone.utc).isoformat(),
                "mode":"mock" if client.mock else "live","config":cfg,
                "categories":tree,"total_prompts":total_prompts[0]}
    _write(build_dir/"manifest.json", manifest)
    (LIB/"LATEST.txt").write_text(stamp)
    print(f"[{now()}] DONE. build={stamp}  total prompts={total_prompts[0]}")
    print(f"        output: {build_dir}")
    return build_dir

# ── CLI ────────────────────────────────────────────────────────────────────
def cmd_list():
    if not BUILDS.exists(): print("No builds yet."); return
    for d in sorted(BUILDS.iterdir()):
        man = d/"manifest.json"
        if man.exists():
            m = json.loads(man.read_text())
            print(f"{d.name}  ·  {m['total_prompts']} prompts  ·  "
                  f"{len(m['categories'])} categories  ·  {m['mode']}")
        else:
            print(f"{d.name}  ·  (incomplete)")

def cmd_list_categories():
    for c in json.loads((ROOT/"seeds.json").read_text())["categories"]:
        print(f"{c['id']:22} {c['family']:11} {c['outcome']}")

def main():
    ap = argparse.ArgumentParser(description="Prompt-forge production engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="forge a fresh dated build")
    b.add_argument("--category", help="one category id (omit + use --all for everything)")
    b.add_argument("--all", action="store_true")
    b.add_argument("--subs", type=int, default=8)
    b.add_argument("--subsubs", type=int, default=5)
    b.add_argument("--leaf-prompts", type=int, default=50)
    b.add_argument("--sub-prompts", type=int, default=24)
    b.add_argument("--cat-prompts", type=int, default=12)
    b.add_argument("--chunk", type=int, default=10, help="prompts per API call")
    b.add_argument("--concurrency", type=int, default=4)
    b.add_argument("--model", default="claude-sonnet-4-6")
    b.add_argument("--max-tokens", type=int, default=6000)
    b.add_argument("--dry-run", action="store_true")

    sub.add_parser("list", help="list dated builds")
    sub.add_parser("list-categories", help="list seed categories")
    a = ap.parse_args()

    if a.cmd=="list": return cmd_list()
    if a.cmd=="list-categories": return cmd_list_categories()

    if a.cmd=="build":
        if not a.category and not a.all:
            raise SystemExit("Choose scope: --category <id>  OR  --all")
        cfg = {"category": None if a.all else a.category, "subs":a.subs,"subsubs":a.subsubs,
               "leaf_prompts":a.leaf_prompts,"sub_prompts":a.sub_prompts,"cat_prompts":a.cat_prompts,
               "chunk":a.chunk,"concurrency":a.concurrency,"model":a.model,"mx":a.max_tokens,
               "mock": a.dry_run or not os.getenv("ANTHROPIC_API_KEY")}
        if cfg["mock"] and not a.dry_run:
            print("No ANTHROPIC_API_KEY -> MOCK mode. Set the key for real content.")
        asyncio.run(run(cfg))

if __name__ == "__main__":
    main()
