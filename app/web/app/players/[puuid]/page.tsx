'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/Layout';
import { getPlayerProfile, type PlayerProfile } from '@/lib/api';

function MetricCard({
  label,
  value,
  suffix = '',
}: {
  label: string;
  value: string | number;
  suffix?: string;
}) {
  return (
    <div className="p-4 rounded-xl bg-zinc-800/50 border border-zinc-700/50">
      <p className="text-sm text-zinc-400">{label}</p>
      <p className="text-2xl font-bold text-zinc-100 mt-1">
        {value}
        {suffix}
      </p>
    </div>
  );
}

export default function PlayerProfilePage() {
  const params = useParams();
  const puuid = params.puuid as string;
  const [profile, setProfile] = useState<PlayerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!puuid) return;
    getPlayerProfile(puuid)
      .then(setProfile)
      .catch((err) => setError(err instanceof Error ? err.message : 'Erro'))
      .finally(() => setLoading(false));
  }, [puuid]);

  if (loading) {
    return (
      <Layout>
        <div className="p-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-zinc-700 rounded w-1/3" />
            <div className="h-32 bg-zinc-700 rounded" />
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-20 bg-zinc-700 rounded" />
              ))}
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !profile) {
    return (
      <Layout>
        <div className="p-8">
          <p className="text-red-400 mb-4">{error || 'Perfil não encontrado'}</p>
          <Link href="/players" className="text-primary hover:underline">
            Voltar e sincronizar jogador
          </Link>
        </div>
      </Layout>
    );
  }

  const { player, metrics } = profile;
  const winrateColor =
    metrics.winrate >= 55 ? 'text-accent' : metrics.winrate >= 50 ? 'text-yellow-400' : 'text-red-400';

  return (
    <Layout>
      <div className="p-8">
        <div className="flex items-center gap-4 mb-6">
          <Link href="/players" className="text-zinc-400 hover:text-zinc-100 text-sm">
            ← Jogadores
          </Link>
        </div>

        <h1 className="text-2xl font-bold text-zinc-100 mb-1">{player.summoner_name}</h1>
        <p className="text-zinc-500 text-sm mb-6">{player.region.toUpperCase()}</p>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <MetricCard label="Partidas" value={metrics.matches} />
          <div className="p-4 rounded-xl bg-zinc-800/50 border border-zinc-700/50">
            <p className="text-sm text-zinc-400">Winrate</p>
            <p className={`text-2xl font-bold mt-1 ${winrateColor}`}>
              {metrics.winrate.toFixed(1)}%
            </p>
          </div>
          <MetricCard label="KDA médio" value={metrics.avg_kda.toFixed(2)} />
          <MetricCard label="CS/min" value={metrics.avg_cs_per_min.toFixed(2)} />
          <MetricCard label="Vision Score" value={metrics.avg_vision_score.toFixed(1)} />
        </div>

        <p className="text-xs text-zinc-600">
          Última atualização: {new Date(profile.updated_at).toLocaleString('pt-BR')}
        </p>
      </div>
    </Layout>
  );
}
