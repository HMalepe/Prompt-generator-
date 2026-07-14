"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Overview" },
  { href: "/dashboard/categories", label: "Categories" },
  { href: "/dashboard/forge", label: "Forge" },
  { href: "/dashboard/packs", label: "Packs" },
];

export function DashboardNav() {
  const pathname = usePathname();

  return (
    <aside className="dash-nav">
      <Link href="/" className="brand-mark">
        <span className="brand-ember" aria-hidden />
        <span>
          Prompt <em>Forge</em>
        </span>
      </Link>
      <nav>
        {links.map((l) => {
          const active =
            l.href === "/dashboard"
              ? pathname === "/dashboard"
              : pathname.startsWith(l.href);
          return (
            <Link
              key={l.href}
              href={l.href}
              className={active ? "nav-link active" : "nav-link"}
            >
              {l.label}
            </Link>
          );
        })}
      </nav>
      <p className="nav-footnote">
        Engine stays local. This board designs runs and reviews packs.
      </p>
    </aside>
  );
}
