import DashboardClient from "./components/DashboardClient.jsx";
import { getDashboardData } from "@/lib/dashboard-data.js";

export const dynamic = "force-dynamic";

export default function Home() {
  const data = getDashboardData();
  return <DashboardClient data={data} />;
}
