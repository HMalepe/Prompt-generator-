import { DashboardNav } from "@/components/DashboardNav";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dash">
      <DashboardNav />
      <div className="dash-main">{children}</div>
    </div>
  );
}
