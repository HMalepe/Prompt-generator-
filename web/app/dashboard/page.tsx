import Link from "next/link";
import { categories, FAMILIES, leafPack, manifest } from "@/lib/catalog";

export default function DashboardPage() {
  return (
    <>
      <header className="page-head">
        <h1>Overview</h1>
        <p>
          Internal production board for Prompt Forge. Seed catalog and a sample
          dated build are loaded for review; heavy forging still runs on your
          machine.
        </p>
      </header>

      <div className="grid-stats">
        <div className="stat-tile">
          <strong>{categories.length}</strong>
          <span>seed categories</span>
        </div>
        <div className="stat-tile">
          <strong>{FAMILIES.length}</strong>
          <span>families</span>
        </div>
        <div className="stat-tile">
          <strong>{manifest.total_prompts}</strong>
          <span>prompts in sample build</span>
        </div>
      </div>

      <section className="panel">
        <h2>Latest sample build</h2>
        <div className="stat-line">
          <span>Stamp</span>
          <span>{manifest.build}</span>
        </div>
        <div className="stat-line">
          <span>Mode</span>
          <span>{manifest.mode}</span>
        </div>
        <div className="stat-line">
          <span>Featured leaf</span>
          <span>
            {leafPack.category} / {leafPack.subcategory} / {leafPack.leaf}
          </span>
        </div>
        <div style={{ marginTop: "1rem" }}>
          <Link href="/dashboard/packs/sample" className="btn btn-primary">
            Open sample pack
          </Link>
        </div>
      </section>

      <section className="panel">
        <h2>Quick paths</h2>
        <div className="cta-row">
          <Link href="/dashboard/categories" className="btn btn-ghost">
            Browse categories
          </Link>
          <Link href="/dashboard/forge" className="btn btn-ghost">
            Size a forge run
          </Link>
          <Link href="/dashboard/packs" className="btn btn-ghost">
            Review packs
          </Link>
        </div>
      </section>
    </>
  );
}
