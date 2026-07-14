"use client";

import { useMemo, useState } from "react";
import { categories, estimateCalls, forgeCommand } from "@/lib/catalog";
import { CopyButton } from "@/components/CopyButton";

export function ForgePanel() {
  const [category, setCategory] = useState(categories[0]?.id ?? "websites");
  const [dryRun, setDryRun] = useState(true);
  const [subs, setSubs] = useState(2);
  const [subsubs, setSubsubs] = useState(2);
  const [leafPrompts, setLeafPrompts] = useState(50);

  const estimate = useMemo(
    () =>
      estimateCalls({
        subs,
        subsubs,
        leafPrompts,
        subPrompts: 24,
        catPrompts: 12,
        chunk: 10,
      }),
    [subs, subsubs, leafPrompts],
  );

  const cmd = forgeCommand({
    category,
    dryRun,
    all: false,
    subs,
    subsubs,
    leafPrompts,
  });

  return (
    <div className="forge-panel">
      <div className="field-grid">
        <label className="field">
          <span>Category</span>
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.id}
              </option>
            ))}
          </select>
        </label>
        <label className="field check">
          <input
            type="checkbox"
            checked={dryRun}
            onChange={(e) => setDryRun(e.target.checked)}
          />
          <span>Dry-run (mock, free)</span>
        </label>
        <label className="field">
          <span>Subcategories · {subs}</span>
          <input
            type="range"
            min={1}
            max={8}
            value={subs}
            onChange={(e) => setSubs(Number(e.target.value))}
          />
        </label>
        <label className="field">
          <span>Leaves per sub · {subsubs}</span>
          <input
            type="range"
            min={1}
            max={5}
            value={subsubs}
            onChange={(e) => setSubsubs(Number(e.target.value))}
          />
        </label>
        <label className="field">
          <span>Prompts per leaf · {leafPrompts}</span>
          <input
            type="range"
            min={6}
            max={50}
            step={2}
            value={leafPrompts}
            onChange={(e) => setLeafPrompts(Number(e.target.value))}
          />
        </label>
      </div>

      <div className="estimate-row">
        <div>
          <strong>{estimate.leaves}</strong>
          <span>leaf packs</span>
        </div>
        <div>
          <strong>{estimate.totalPrompts.toLocaleString()}</strong>
          <span>prompts</span>
        </div>
        <div>
          <strong>~{estimate.calls}</strong>
          <span>API calls{dryRun ? " (skipped)" : ""}</span>
        </div>
      </div>

      <div className="cmd-box">
        <code>{cmd}</code>
        <CopyButton text={cmd} label="Copy command" />
      </div>

      {!dryRun && estimate.calls > 80 && (
        <p className="warn">
          Live run at this fan-out is minutes and real dollars. Prefer a small
          scoped build first.
        </p>
      )}
    </div>
  );
}
