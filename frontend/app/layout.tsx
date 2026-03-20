import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BizPilot AI - Business Operating System",
  description: "AI-powered business analysis and reporting",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen">{children}</body>
    </html>
  );
}
