# Arquitetura do DraftVision

## Visão geral

O DraftVision é uma plataforma de análise estratégica de jogadores e times de League of Legends, baseada em dados da API da Riot Games. O sistema segue **Clean Architecture** e princípios **SOLID**, com separação clara de camadas.

```
Web App
   ↓
API
   ↓
Application Layer (Use Cases)
   ↓
Domain Layer (Entities, Value Objects)
   ↓
Infrastructure (DB, Cache, Riot API)
   ↓
Database / Cache / Riot API
```

## Stack tecnológica

| Camada | Tecnologia | Responsabilidade |
|--------|------------|------------------|
| **Frontend** | Next.js, TailwindCSS, Chart.js | Dashboard, visualização, comparação, gestão de times |
| **Backend** | Python, FastAPI, Pydantic | Integração Riot, processamento, cálculos, relatórios |
| **Processamento** | pandas, numpy | Análise de partidas, métricas, classificação |
| **Banco** | PostgreSQL | Persistência de dados |
| **Cache** | Redis | Evitar rate limit da API Riot |

## Estrutura de código (Clean Architecture)

```
draftvision/
├── app/
│   ├── api/
│   │   └── src/
│   │       ├── domain/
│   │       │   ├── entities/
│   │       │   │   ├── player.py
│   │       │   │   ├── match.py
│   │       │   │   └── team.py
│   │       │   ├── value_objects/
│   │       │   │   ├── kda.py
│   │       │   │   └── player_score.py
│   │       │   └── interfaces/
│   │       │       ├── player_repository.py
│   │       │       ├── match_repository.py
│   │       │       └── riot_service.py
│   │       │
│   │       ├── application/
│   │       │   ├── use_cases/
│   │       │   │   ├── get_player_profile.py
│   │       │   │   ├── analyze_player.py
│   │       │   │   ├── compare_players.py
│   │       │   │   └── create_team.py
│   │       │   └── services/
│   │       │       └── player_analysis_service.py
│   │       │
│   │       ├── infrastructure/
│   │       │   ├── database/
│   │       │   │   ├── models/
│   │       │   │   │   ├── player_model.py
│   │       │   │   │   ├── match_model.py
│   │       │   │   │   └── team_model.py
│   │       │   │   └── database.py
│   │       │   ├── repositories/
│   │       │   │   ├── player_repository_impl.py
│   │       │   │   └── match_repository_impl.py
│   │       │   ├── riot_api/
│   │       │   │   └── riot_client.py
│   │       │   └── cache/
│   │       │       └── redis_cache.py
│   │       │
│   │       ├── interfaces/
│   │       │   ├── controllers/
│   │       │   │   ├── player_controller.py
│   │       │   │   ├── team_controller.py
│   │       │   │   └── analysis_controller.py
│   │       │   └── routes/
│   │       │       ├── player_routes.py
│   │       │       └── team_routes.py
│   │       │
│   │       └── main.py
│   │
│   └── web/
│       ├── src/
│       ├── pages/
│       │   ├── dashboard/
│       │   ├── players/
│       │   ├── teams/
│       │   └── scouting/
│       ├── components/
│       │   ├── charts/
│       │   ├── tables/
│       │   └── player_cards/
│       ├── services/
│       │   └── api_client.ts
│       └── styles/
│
├── workers/
│   └── match_collector.py
├── docs/
└── .github/workflows/
```

## Camadas

### Domain
- **Entities**: Player, Match, Team
- **Value Objects**: KDA, PlayerScore
- **Interfaces**: Contratos (repositories, services) que a infraestrutura implementa

### Application
- **Use Cases**: Get player profile, Analyze player, Compare players, Create team
- **Services**: Lógica de negócio (ex: PlayerAnalysisService)

### Infrastructure
- **Database**: Modelos SQLAlchemy, conexão
- **Repositories**: Implementações concretas dos repositórios
- **Riot API**: Cliente HTTP com cache
- **Cache**: Redis para dados da Riot

### Interfaces
- **Controllers**: Orquestram use cases e retornam respostas HTTP
- **Routes**: Definição das rotas FastAPI

## Worker de coleta

O `workers/match_collector.py` é responsável por:

1. Buscar jogadores monitorados
2. Coletar novas partidas
3. Atualizar banco de dados
4. Recalcular métricas

Execução via: **cron**, **queue** ou **background worker**.

## Fluxo de dados

### Coleta (Riot → Cache → DB)
```
Riot API ──► Redis (cache) ──► Backend ──► PostgreSQL
```

### Análise
```
PostgreSQL ──► pandas/numpy ──► Insights, PlayerScore
```

### Serviço ao frontend
```
Frontend ──► API Backend ──► Redis/PostgreSQL ──► JSON
```

## Referências

- [DATABASE.md](./DATABASE.md) — Modelagem do banco
- [API_RIOT.md](./API_RIOT.md) — Fluxo e endpoints Riot
- [ALGORITHMS.md](./ALGORITHMS.md) — PlayerScore e métricas
