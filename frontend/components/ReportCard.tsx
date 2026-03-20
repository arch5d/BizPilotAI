"use client";

interface Report {
  id: number;
  agent_name: string;
  content: string;
  created_at: string;
}

interface ReportCardProps {
  report: Report;
}

export default function ReportCard({ report }: ReportCardProps) {
  const formattedDate = new Date(report.created_at).toLocaleString();

  return (
    <article className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow">
      <div className="p-4 border-b border-slate-100 bg-slate-50">
        <div className="flex justify-between items-center">
          <span className="text-xs font-medium text-primary-600 bg-primary-50 px-2 py-1 rounded">
            {report.agent_name}
          </span>
          <span className="text-xs text-slate-500">{formattedDate}</span>
        </div>
      </div>
      <div className="p-4">
        <pre className="text-sm text-slate-700 whitespace-pre-wrap font-sans max-h-48 overflow-y-auto">
          {report.content}
        </pre>
      </div>
    </article>
  );
}
