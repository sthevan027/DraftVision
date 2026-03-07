# API Riot e rate limits

## Visão geral

O DraftVision depende da [Riot Games API](https://developer.riotgames.com/) para obter dados de jogadores e partidas. A API tem **rate limits rígidos** que exigem cache obrigatório.

## Fluxo de coleta

```
buscar jogador
   ↓
obter PUUID
   ↓
buscar partidas
   ↓
coletar dados da partida
   ↓
salvar no banco
   ↓
calcular métricas
```

## APIs utilizadas

| API | Uso |
|-----|-----|
| **account-v1** | Resolução de Riot ID para PUUID |
| **summoner-v4** | Dados do summoner (PUUID, accountId) |
| **league-v4** | Rank, LP, divisão |
| **match-v5** | Partidas e detalhes |

## Autenticação

- **API Key**: Obtenha em [Riot Developer Portal](https://developer.riotgames.com/)
- **Validade**: Keys de desenvolvimento expiram em 24h; produção usa keys permanentes
- **Header**: `X-Riot-Token: <sua-api-key>`

## Endpoints utilizados

| Endpoint | Uso | Rate limit (dev) |
|----------|-----|------------------|
| `/lol/summoner/v4/summoners/by-puuid/{puuid}` | Buscar jogador por PUUID | 20 req/s |
| `/lol/summoner/v4/summoners/by-name/{name}` | Buscar jogador por nome | 20 req/s |
| `/lol/match/v5/matches/by-puuid/{puuid}/ids` | IDs de partidas do jogador | 20 req/s |
| `/lol/match/v5/matches/{matchId}` | Detalhes da partida | 100 req/2min |
| `/lol/league/v4/entries/by-summoner/{id}` | Rank e LP | 20 req/s |

## Regiões

| Código | Região |
|--------|--------|
| br1 | Brasil |
| na1 | América do Norte |
| kr | Coreia |
| euw1 | Europa Oeste |
| eun1 | Europa Norte e Leste |

Base URL: `https://{region}.api.riotgames.com`

## Rate limits

- **20 requests/segundo** para a maioria dos endpoints
- **100 requests/2 minutos** para match detail (endpoint mais restritivo)
- Headers de resposta: `X-App-Rate-Limit-Count`, `Retry-After` (em 429)

## Estratégia de cache (obrigatório)

| Dado | TTL Redis | Motivo |
|------|-----------|--------|
| Summoner (puuid, accountId) | 5 min | Pouco variável |
| League entries (rank) | 15 min | Atualiza com frequência |
| Match IDs (lista) | 30 min | Cresce com o tempo |
| Match detail | 2h+ | Imutável após a partida |

## Implementação recomendada

```python
# Exemplo de fluxo com cache
async def get_summoner(name: str, region: str) -> Summoner:
    cache_key = f"summoner:{region}:{name}"
    cached = await redis.get(cache_key)
    if cached:
        return Summoner.model_validate_json(cached)
    
    data = await riot_client.get_summoner_by_name(name, region)
    await redis.setex(cache_key, 300, data.model_dump_json())
    return data
```

## Retry e backoff

- Status **429**: Respeitar header `Retry-After`
- Status **503**: Backoff exponencial (1s, 2s, 4s, …)
- Máximo de 3 retentativas por requisição

## Referências

- [Riot API Documentation](https://developer.riotgames.com/apis)
- [Rate Limiting](https://developer.riotgames.com/docs/portal#web-apis_rate-limiting)
