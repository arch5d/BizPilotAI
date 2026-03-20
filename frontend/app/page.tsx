"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import RunMarketingAgentButton from "@/components/RunMarketingAgentButton";
import ReportCard from "@/components/ReportCard";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Report {
  id: number;
  agent_name: string;
  content: string;
  created_at: string;
}

export default function DashboardPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async () => {
    try {
      const res = await fetch(`${API_URL}/reports`);
      if (!res.ok) throw new Error("Failed to fetch reports");
      const data = await res.json();
      setReports(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 bg-slate-50">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-6">
            BizPilot AI Dashboard
          </h1>

          <section className="mb-10">
            <h2 className="text-lg font-semibold text-slate-700 mb-4">
              Run Agents
            </h2>
            <RunMarketingAgentButton onSuccess={fetchReports} />
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-700 mb-4">
              Reports
            </h2>
            {loading ? (
              <p className="text-slate-500">Loading reports...</p>
            ) : error ? (
              <p className="text-red-600">{error}</p>
            ) : reports.length === 0 ? (
              <p className="text-slate-500">
                No reports yet. Run the Marketing Agent to generate your first report.
              </p>
            ) : (
              <div className="space-y-4">
                {reports.map((report) => (
                  <ReportCard key={report.id} report={report} />
                ))}
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
