"use client";

import Sidebar from "@/components/Sidebar";

export default function AgentsPage() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 bg-slate-50">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-6">Agents</h1>
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-700 mb-2">
              Marketing Trend Agent
            </h2>
            <p className="text-slate-600 mb-4">
              Analyzes and summarizes business and AI trends. Run from the Dashboard.
            </p>
            <a
              href="/"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              Go to Dashboard →
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
