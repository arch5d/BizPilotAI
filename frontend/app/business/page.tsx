"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Business {
  id: number;
  name: string;
  industry: string | null;
  website: string | null;
  description: string | null;
  goals: string | null;
  created_at: string;
}

const emptyForm = {
  name: "",
  industry: "",
  website: "",
  description: "",
  goals: "",
};

export default function BusinessProfilePage() {
  const [form, setForm] = useState(emptyForm);
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const fetchBusinesses = async () => {
    try {
      const res = await fetch(`${API_URL}/business`);
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setBusinesses(data);
    } catch {
      setMessage({ type: "error", text: "Failed to load business profiles" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBusinesses();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    try {
      const res = await fetch(`${API_URL}/business/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name.trim(),
          industry: form.industry.trim() || null,
          website: form.website.trim() || null,
          description: form.description.trim() || null,
          goals: form.goals.trim() || null,
        }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to create");
      }
      setMessage({ type: "success", text: "Business profile created successfully." });
      setForm(emptyForm);
      fetchBusinesses();
    } catch (err) {
      setMessage({
        type: "error",
        text: err instanceof Error ? err.message : "Something went wrong",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 bg-slate-50">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-6">Business Profile</h1>
          <p className="text-slate-600 mb-8">
            Add your company info to get personalized reports from the Marketing Agent. Website content is scraped and stored for context.
          </p>

          <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 mb-8">
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">
                  Company name *
                </label>
                <input
                  id="name"
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Acme Inc."
                />
              </div>
              <div>
                <label htmlFor="industry" className="block text-sm font-medium text-slate-700 mb-1">
                  Industry
                </label>
                <input
                  id="industry"
                  type="text"
                  value={form.industry}
                  onChange={(e) => setForm((f) => ({ ...f, industry: e.target.value }))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="SaaS, Healthcare, etc."
                />
              </div>
              <div>
                <label htmlFor="website" className="block text-sm font-medium text-slate-700 mb-1">
                  Website
                </label>
                <input
                  id="website"
                  type="url"
                  value={form.website}
                  onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="https://example.com"
                />
              </div>
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-slate-700 mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  rows={3}
                  value={form.description}
                  onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="What your company does..."
                />
              </div>
              <div>
                <label htmlFor="goals" className="block text-sm font-medium text-slate-700 mb-1">
                  Goals
                </label>
                <textarea
                  id="goals"
                  rows={3}
                  value={form.goals}
                  onChange={(e) => setForm((f) => ({ ...f, goals: e.target.value }))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Marketing and business goals..."
                />
              </div>
            </div>
            {message && (
              <p className={`mt-4 text-sm ${message.type === "success" ? "text-green-600" : "text-red-600"}`}>
                {message.text}
              </p>
            )}
            <button
              type="submit"
              disabled={submitting}
              className="mt-6 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? "Creating..." : "Create Business Profile"}
            </button>
          </form>

          <section>
            <h2 className="text-lg font-semibold text-slate-700 mb-4">Your business profiles</h2>
            {loading ? (
              <p className="text-slate-500">Loading...</p>
            ) : businesses.length === 0 ? (
              <p className="text-slate-500">No profiles yet. Create one above to get personalized reports.</p>
            ) : (
              <ul className="space-y-3">
                {businesses.map((b) => (
                  <li
                    key={b.id}
                    className="bg-white rounded-lg border border-slate-200 p-4 flex justify-between items-start"
                  >
                    <div>
                      <span className="font-medium text-slate-900">{b.name}</span>
                      {b.industry && (
                        <span className="ml-2 text-sm text-slate-500">({b.industry})</span>
                      )}
                      {b.website && (
                        <p className="text-sm text-slate-600 mt-1">{b.website}</p>
                      )}
                    </div>
                    <span className="text-xs text-slate-400">ID: {b.id}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
