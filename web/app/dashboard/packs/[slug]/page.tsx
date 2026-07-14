import Link from "next/link";
import { notFound } from "next/navigation";
import { CopyButton } from "@/components/CopyButton";
import { leafPack } from "@/lib/catalog";

export default async function PackDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  if (slug !== "sample") notFound();

  return (
    <>
      <header className="page-head">
        <p style={{ marginBottom: "0.5rem" }}>
          <Link href="/dashboard/packs" className="btn btn-ghost">
            ← Packs
          </Link>
        </p>
        <h1>{leafPack.leaf}</h1>
        <p>
          {leafPack.category} / {leafPack.subcategory} · {leafPack.difficulty} ·{" "}
          {leafPack.one_liner}
        </p>
      </header>

      {leafPack.prompts.map((step) => (
        <article key={step.step} className="prompt-card">
          <header>
            <h3>
              Step {step.step}: {step.goal}
            </h3>
            <CopyButton text={step.prompt} label="Copy prompt" />
          </header>
          <pre className="prompt-body">{step.prompt}</pre>
          <p className="meta-line">
            Fill-in: {step.fill_in} · Expected: {step.expected}
          </p>
        </article>
      ))}
    </>
  );
}
