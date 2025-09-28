import "./globals.css";
import type { Metadata } from "next";
import { Sidebar } from "@/app/components/Sidebar";

export const metadata: Metadata = {
  title: "Flicaster",
  description: "航空需要予測アプリ",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja" suppressHydrationWarning>
      <body className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </body>
    </html>
  );
}
