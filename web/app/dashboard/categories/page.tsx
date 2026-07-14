import { categories } from "@/lib/catalog";

export default function CategoriesPage() {
  return (
    <>
      <header className="page-head">
        <h1>Categories</h1>
        <p>
          Level-1 seeds from <code>seeds.json</code>. Family chooses the
          meta-prompt fuel; outcome and seed steer expansion.
        </p>
      </header>

      <div className="cat-grid">
        {categories.map((c) => (
          <article key={c.id} className="cat-tile">
            <span className="family">{c.family}</span>
            <h3>{c.id}</h3>
            <p>
              {c.outcome}
              <br />
              Seed: {c.seed}
            </p>
          </article>
        ))}
      </div>
    </>
  );
}
