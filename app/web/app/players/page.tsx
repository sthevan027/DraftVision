'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import { syncPlayer } from '@/lib/api';

export default function PlayersPage() {
  const router = useRouter();
  const [gameName, setGameName] = useState('');
  const [tagLine, setTagLine] = useState('');
  const [region, setRegion] = useState('br1');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await syncPlayer({ game_name: gameName, tag_line: tagLine, region });
      router.push(`/players/${res.puuid}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao sincronizar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="p-8">
        <h1 className="text-2xl font-bold text-zinc-100 mb-6">Sincronizar Jogador</h1>

        <form onSubmit={handleSubmit} className="max-w-md space-y-4">
          <div>
            <label className="block text-sm text-zinc-400 mb-1">Riot ID (Nome do Jogo)</label>
            <input
              type="text"
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              placeholder="Faker"
              className="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-600 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-zinc-400 mb-1">Tag Line</label>
            <input
              type="text"
              value={tagLine}
              onChange={(e) => setTagLine(e.target.value)}
              placeholder="KR1"
              className="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-600 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-zinc-400 mb-1">Região</label>
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-600 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="br1">BR1</option>
              <option value="na1">NA1</option>
              <option value="kr">KR</option>
              <option value="euw1">EUW1</option>
              <option value="eun1">EUN1</option>
              <option value="la1">LA1</option>
              <option value="la2">LA2</option>
            </select>
          </div>
          {error && (
            <div className="p-3 rounded-lg bg-red-500/20 text-red-400 text-sm">{error}</div>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Sincronizando...' : 'Sincronizar e ver perfil'}
          </button>
        </form>

        <p className="mt-6 text-sm text-zinc-500 max-w-md">
          Insira o Riot ID do jogador (ex: Faker#KR1). O sistema buscará as últimas 20 partidas
          ranqueadas e calculará as métricas.
        </p>
      </div>
    </Layout>
  );
}
