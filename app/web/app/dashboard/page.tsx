'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Layout from '@/components/Layout';
import { healthCheck } from '@/lib/api';

export default function DashboardPage() {
  const [apiOk, setApiOk] = useState<boolean | null>(null);

  useEffect(() => {
    healthCheck().then(setApiOk);
  }, []);

  return (
    <Layout>
      <div className="p-8">
        <h1 className="text-2xl font-bold text-zinc-100 mb-6">Dashboard</h1>

        <div className="grid gap-4 md:grid-cols-2 mb-8">
          <div className="p-6 rounded-xl bg-zinc-800/50 border border-zinc-700/50">
            <h3 className="text-sm text-zinc-400 mb-1">Status da API</h3>
            <p className="text-xl font-semibold">
              {apiOk === null ? (
                <span className="text-zinc-500">Verificando...</span>
              ) : apiOk ? (
                <span className="text-accent">Conectado</span>
              ) : (
                <span className="text-red-400">Desconectado</span>
              )}
            </p>
            <p className="text-xs text-zinc-600 mt-2">
              {apiOk === false &&
                'Certifique-se de que o backend está rodando em localhost:8000'}
            </p>
          </div>

          <Link
            href="/players"
            className="p-6 rounded-xl bg-primary/20 border border-primary/40 hover:bg-primary/30 transition-colors block"
          >
            <h3 className="text-sm text-primary mb-1">Sincronizar jogador</h3>
            <p className="text-zinc-300 text-sm">
              Busque um jogador pelo Riot ID e analise as últimas 20 partidas ranqueadas
            </p>
          </Link>
        </div>

        <div className="rounded-xl bg-zinc-800/30 border border-zinc-700/50 p-6">
          <h3 className="text-lg font-semibold text-zinc-100 mb-2">V1 — Funcionalidades</h3>
          <ul className="space-y-2 text-sm text-zinc-400">
            <li className="flex items-center gap-2">
              <span className="text-accent">✓</span> Integração Riot API (account-v1, match-v5)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-accent">✓</span> Perfil de jogador com métricas
            </li>
            <li className="flex items-center gap-2">
              <span className="text-accent">✓</span> Winrate, KDA, CS/min, Vision Score
            </li>
            <li className="flex items-center gap-2">
              <span className="text-accent">✓</span> Dashboard inicial
            </li>
            <li className="flex items-center gap-2">
              <span className="text-zinc-600">○</span> Times e comparação (V2)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-zinc-600">○</span> Scouting e draft (V3)
            </li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
