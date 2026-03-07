# Guia de desenvolvimento – DraftVision

## Pré-requisitos

- **Python 3.11+**
- **Node.js 20+**
- **pnpm** (gerenciador de pacotes do frontend)
- **PostgreSQL 15+**
- **Redis 7+**
- **Chave da Riot API** ([developer.riotgames.com](https://developer.riotgames.com/))

## Configuração do ambiente

### 1. Clone e estrutura

```bash
git clone https://github.com/sthev/DraftVision.git
cd DraftVision
```

### 2. Backend (Python)

```bash
cd app/api
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edite .env com suas variáveis
```

### 3. Frontend (Next.js)

```bash
cd app/web
pnpm install
cp .env.example .env.local
```

### 4. Banco e Redis

```bash
# PostgreSQL: crie um banco draftvision
createdb draftvision

# Redis: inicie o servidor
redis-server
```

### 5. Variáveis de ambiente

**Backend (`.env`):**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/draftvision
REDIS_URL=redis://localhost:6379/0
RIOT_API_KEY=sua-chave-aqui
RIOT_REGION=br1
```

**Frontend (`.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Executando localmente

```bash
# Terminal 1 – Redis (se não estiver rodando)
redis-server

# Terminal 2 – Backend
cd app/api && uvicorn main:app --reload --port 8000

# Terminal 3 – Frontend
cd app/web && pnpm dev
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs da API: http://localhost:8000/docs

## Estrutura de código

### Backend

- `main.py`: App FastAPI, rotas raiz
- `api/riot/`: Cliente Riot, cache, rate limit
- `api/players/`: CRUD jogadores, métricas
- `api/matches/`: Fetch e processamento de partidas
- `api/teams/`: Times, rosters, sinergia
- `api/analytics/`: Insights, PlayerScore, comparações
- `api/scouting/`: Hidden Talent, scouting

### Frontend

- `app/`: Rotas Next.js (App Router)
- `components/`: Componentes reutilizáveis
- `lib/`: Utilitários, fetch da API
- `styles/`: CSS global, Tailwind

## Convenções

- **Python**: Black + Ruff (lint/format)
- **TypeScript**: ESLint + Prettier
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **Branches**: `main` (produção), `develop` (dev), `feature/...`, `fix/...`

## Testes

```bash
# Backend
cd app/api && pytest

# Frontend
cd app/web && pnpm test
```

## Migrações (futuro)

Com Alembic ou similar:

```bash
cd app/api
alembic revision -m "descricao"
alembic upgrade head
```

## Debug

- Backend: logs em stdout; variável `LOG_LEVEL=DEBUG`
- Frontend: React DevTools, console
- Redis: `redis-cli MONITOR` para ver operações
- Riot: Log de requisições e cache hits para debug de rate limit
