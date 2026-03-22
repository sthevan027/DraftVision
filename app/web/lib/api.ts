const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SyncPlayerPayload {
  game_name: string;
  tag_line: string;
  region?: string;
}

export interface SyncPlayerResponse {
  puuid: string;
  matches_synced: number;
  status: string;
}

export interface PlayerProfile {
  player: {
    puuid: string;
    summoner_name: string;
    region: string;
  };
  metrics: {
    matches: number;
    winrate: number;
    avg_kda: number;
    avg_cs_per_min: number;
    avg_vision_score: number;
  };
  updated_at: string;
}

export async function syncPlayer(payload: SyncPlayerPayload): Promise<SyncPlayerResponse> {
  const res = await fetch(`${API_URL}/players/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...payload, region: payload.region || 'br1' }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Sync failed: ${res.status}`);
  }
  return res.json();
}

export async function getPlayerProfile(puuid: string): Promise<PlayerProfile> {
  const res = await fetch(`${API_URL}/players/${puuid}/profile`);
  if (!res.ok) {
    if (res.status === 404) throw new Error('Jogador não encontrado');
    throw new Error(`Falha ao carregar perfil: ${res.status}`);
  }
  return res.json();
}

export async function healthCheck(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
