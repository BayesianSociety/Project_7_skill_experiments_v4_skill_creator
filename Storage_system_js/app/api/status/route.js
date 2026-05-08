import { getDashboardData } from "@/lib/dashboard-data.js";

export const dynamic = "force-dynamic";

export function GET() {
  const data = getDashboardData();
  return Response.json(data.status);
}
