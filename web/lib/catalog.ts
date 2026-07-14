import seeds from "@/data/seeds.json";
import sampleLeaf from "@/data/sample-leaf.json";
import sampleManifest from "@/data/sample-manifest.json";
import type { BuildManifest, Category, LeafPack } from "@/lib/types";

export const categories = (seeds as { categories: Category[] }).categories;
export const leafPack = sampleLeaf as LeafPack;
export const manifest = sampleManifest as BuildManifest;

export const FAMILIES = Array.from(
  new Set(categories.map((c) => c.family)),
).sort();

export function estimateCalls(opts: {
  subs: number;
  subsubs: number;
  leafPrompts: number;
  subPrompts: number;
  catPrompts: number;
  chunk: number;
}) {
  const leaves = opts.subs * opts.subsubs;
  const leafCalls = leaves * Math.ceil(opts.leafPrompts / opts.chunk);
  const subCalls = opts.subs * Math.ceil(opts.subPrompts / opts.chunk);
  const catCalls = Math.ceil(opts.catPrompts / opts.chunk);
  // plus a few structure calls for subcategory naming etc. — rough lower bound
  const structure = 1 + opts.subs;
  return {
    leaves,
    totalPrompts:
      opts.catPrompts + opts.subs * opts.subPrompts + leaves * opts.leafPrompts,
    calls: leafCalls + subCalls + catCalls + structure,
  };
}

export function forgeCommand(opts: {
  category: string;
  dryRun: boolean;
  all: boolean;
  subs: number;
  subsubs: number;
  leafPrompts: number;
}) {
  const parts = ["python forge.py build"];
  if (opts.all) parts.push("--all");
  else parts.push(`--category ${opts.category}`);
  if (opts.dryRun) parts.push("--dry-run");
  parts.push(`--subs ${opts.subs}`);
  parts.push(`--subsubs ${opts.subsubs}`);
  parts.push(`--leaf-prompts ${opts.leafPrompts}`);
  return parts.join(" ");
}
