import { getDashboardData } from "@/lib/dashboard-data.js";

export const dynamic = "force-dynamic";

export async function GET(_request, context) {
  const params = await context.params;
  const data = getDashboardData();
  const detail = data.runDetails[params.runUid];
  if (!detail) {
    return Response.json({ error: "Run not found" }, { status: 404 });
  }
  return Response.json(detail);
}
