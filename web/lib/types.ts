export type Category = {
  id: string;
  family: string;
  outcome: string;
  seed: string;
};

export type PromptStep = {
  step: number;
  goal: string;
  prompt: string;
  fill_in: string;
  expected: string;
};

export type LeafPack = {
  category: string;
  subcategory: string;
  leaf: string;
  one_liner: string;
  difficulty: string;
  prompt_count: number;
  prompts: PromptStep[];
};

export type BuildManifest = {
  build: string;
  generated: string;
  mode: string;
  config: Record<string, unknown>;
  categories: Record<string, string[]>;
  total_prompts: number;
};
