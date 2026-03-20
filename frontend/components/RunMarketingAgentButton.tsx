"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Business {
  id: number;
  name: string;
  industry: string | null;
}

interface RunMarketingAgentButtonProps {
  onSuccess?: () => void;
}

export default function RunMarketingAgentButton({
  onSuccess,
}: RunMarketingAgentButtonProps) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [selectedBusinessId, setSelectedBusinessId] = useState<string>("");

  useEffect(() => {
    fetch(`${API_URL}/business`)
      .then((res) => res.ok ? res.json() : [])
      .then((data) => setBusinesses(data || []))
      .catch(() => setBusinesses([]));
  }, []);

  const handleRun = async () => {
    setLoading(true);
    setMessage(null);
    setError(null);
    try {
      const url = new URL(`${API_URL}/agents/run/marketing`);
      if (selectedBusinessId) url.searchParams.set("business_id", selectedBusinessId);
      const res = await fetch(url.toString(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to run agent");
      setMessage(data.message || "Report generated successfully!");
      onSuccess?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      {businesses.length > 0 && (
        <div>
          <label htmlFor="business-select" className="block text-sm font-medium text-slate-700 mb-1">
            Use business profile (optional)
          </label>
          <select
            id="business-select"
            value={selectedBusinessId}
            onChange={(e) => setSelectedBusinessId(e.target.value)}
            className="mb-3 w-full max-w-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">No profile (generic report)</option>
            {businesses.map((b) => (
              <option key={b.id} value={b.id}>
                {b.name}{b.industry ? ` (${b.industry})` : ""}
              </option>
            ))}
          </select>
        </div>
      )}
      <button
        onClick={handleRun}
        disabled={loading}
        className="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Running Marketing Agent..." : "Run Marketing Agent"}
      </button>
      {message && (
        <p className="text-sm text-green-600">{message}</p>
      )}
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}
