import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-background flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-zinc-100">DraftVision</h1>
      <p className="mt-4 text-zinc-400 text-center max-w-md">
        Plataforma de análise estratégica de jogadores e times de League of Legends
        para organizações, analistas e coaches.
      </p>
      <div className="mt-8 flex gap-4">
        <Link
          href="/dashboard"
          className="px-6 py-3 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-colors"
        >
          Acessar Dashboard
        </Link>
        <Link
          href="/players"
          className="px-6 py-3 rounded-lg bg-zinc-700 text-zinc-100 font-medium hover:bg-zinc-600 transition-colors"
        >
          Sincronizar Jogador
        </Link>
      </div>
    </main>
  );
}
