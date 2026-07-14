import { ForgePanel } from "@/components/ForgePanel";

export default function ForgePage() {
  return (
    <>
      <header className="page-head">
        <h1>Forge</h1>
        <p>
          Dial fan-out, see call estimates, and copy a ready CLI command. Real
          generations need <code>ANTHROPIC_API_KEY</code> on your local machine —
          Vercel does not run the Python engine.
        </p>
      </header>

      <section className="panel">
        <h2>Run designer</h2>
        <ForgePanel />
      </section>
    </>
  );
}
