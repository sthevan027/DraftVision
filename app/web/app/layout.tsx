import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DraftVision',
  description: 'Plataforma de análise estratégica de LoL para organizações e coaches',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-zinc-900 text-zinc-100 antialiased">
        {children}
      </body>
    </html>
  );
}
