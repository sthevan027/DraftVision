# Worker de Coleta

## Visão geral

O worker `match_collector` é responsável por manter os dados dos jogadores monitorados atualizados.

## Função

1. Buscar jogadores monitorados (tracked)
2. Coletar novas partidas de cada jogador
3. Atualizar banco de dados
4. Recalcular métricas (winrate, KDA, farm/min, etc.)

## Execução

O worker pode ser executado por:

- **Cron**: job agendado (ex: a cada 15 min)
- **Queue**: fila de tarefas (Celery, RQ, etc.)
- **Background worker**: processo contínuo

## Localização

```
workers/
└── match_collector.py
```

## Fluxo

```
Jogadores monitorados
   ↓
Para cada jogador:
   - Buscar match IDs (Riot API)
   - Filtrar partidas novas
   - Fetch detalhes (com cache Redis)
   - Salvar player_matches
   ↓
Recalcular métricas agregadas (players.winrate, kda, etc.)
```

## Rate limit

O worker deve respeitar os limites da API Riot. Usar:

- Cache Redis para partidas já buscadas
- Delay entre requisições
- Retry com backoff em 429
