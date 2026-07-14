import Link from "next/link";
import { categories, manifest } from "@/lib/catalog";

export default function HomePage() {
  return (
    <main className="landing">
      <div className="landing-bg" aria-hidden />
      <div className="landing-shell">
        <header className="topbar">
          <div className="brand-mark">
            <span className="brand-ember" aria-hidden />
            <span>
              Prompt <em>Forge</em>
            </span>
          </div>
          <Link href="/dashboard" className="btn btn-ghost">
            Open dashboard
          </Link>
        </header>

        <section className="hero">
          <h1>
            Prompt <em>Forge</em>
          </h1>
          <p>
            One press forges a dated tree of prompts. Browse categories, size a
            run, then ship leaf packs as Word and PDF.
          </p>
          <div className="cta-row">
            <Link href="/dashboard" className="btn btn-primary">
              Enter dashboard
            </Link>
            <Link href="/dashboard/forge" className="btn btn-ghost">
              Build a forge command
            </Link>
          </div>
        </section>

        <aside className="landing-aside">
          <h2>Live board snapshot</h2>
          <div className="stat-line">
            <span>Seed categories</span>
            <span>{categories.length}</span>
          </div>
          <div className="stat-line">
            <span>Sample build</span>
            <span>{manifest.build}</span>
          </div>
          <div className="stat-line">
            <span>Mode</span>
            <span>{manifest.mode}</span>
          </div>
          <div className="stat-line">
            <span>Prompts in sample</span>
            <span>{manifest.total_prompts}</span>
          </div>
        </aside>
      </div>
    </main>
  );
}
