import Link from "next/link";
import { leafPack, manifest } from "@/lib/catalog";

export default function PacksPage() {
  return (
    <>
      <header className="page-head">
        <h1>Packs</h1>
        <p>
          Leaf packs from the sample dated build. Connect a build sync later to
          list every local forge output here.
        </p>
      </header>

      <section className="panel">
        <h2>Build {manifest.build}</h2>
        <div className="pack-list">
          <Link href="/dashboard/packs/sample" className="pack-row">
            <div>
              <h3>
                {leafPack.leaf}
              </h3>
              <p>
                {leafPack.category} · {leafPack.subcategory} · {leafPack.one_liner}
              </p>
            </div>
            <span className="badge">{leafPack.prompt_count} prompts</span>
          </Link>
        </div>
      </section>
    </>
  );
}
