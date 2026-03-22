# Status atual do projeto (diagnóstico rápido)

## O que já foi feito (V1 completo)

### Estrutura e direcionamento
- Repositório organizado com backend (`app/api`), frontend (`app/web`) e documentação.
- Visão de produto, arquitetura, banco, roadmap e guias de desenvolvimento.

### Backend (V1 implementado)
- API FastAPI com CORS para frontend local.
- **PostgreSQL**: modelos SQLAlchemy, repositório async, migrações Alembic.
- **Redis**: cache de perfil (TTL 5 min), invalidação no sync.
- **Riot API**: cliente real (account-v1, match-v5) com retry/backoff para 429 e 503.
- Endpoints: `POST /players/sync`, `GET /players/{puuid}/profile`.
- Fallback para MockRiotClient quando RIOT_API_KEY não está definida.
- Testes automatizados para métricas, fluxo sync/profile e idempotência.

### Frontend (V1 implementado)
- Next.js com App Router, Tailwind, design system (cores do dashboard-design).
- Página inicial, Dashboard (status API), Sincronizar jogador, Perfil com métricas.
- API client (sync, getProfile, healthCheck).
- Sidebar e layout com navegação.

## O que falta (V2+)

### Funcionalidades de negócio (V2 e V3)
- Gestão de times e comparação de jogadores.
- Champion pool analysis.
- Scouting automático, Hidden Talent Detector e análise de draft.

### Backend técnico (evolução)
- Módulos `api/teams`, `api/scouting` (V2/V3).
- Migrations para seeds de desenvolvimento.

### Frontend técnico (evolução)
- Rotas teams, draft e reports (V2/V3).
- Gráficos com Chart.js para tendências e evolução.

### Qualidade e operação
- CI já configurado (lint + testes backend, build frontend).
- Expandir testes de integração com PostgreSQL/Redis.

## Próximos passos (V2)
1. Criação de times e rosters.
2. Comparação entre jogadores.
3. Champion pool analysis.
