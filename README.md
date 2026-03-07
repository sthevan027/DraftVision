# DraftVision

> Plataforma de análise estratégica de jogadores e times de League of Legends para organizações de esports, analistas e coaches profissionais.

[![CI](https://github.com/sthevan027/DraftVision/actions/workflows/ci.yml/badge.svg)](https://github.com/sthevan027/DraftVision/actions/workflows/ci.yml)

## Objetivo

Centralizar análise de performance que hoje é feita em várias ferramentas (OP.GG, Excel, anotações manuais) em uma única plataforma com **análise estratégica**, **scouting** e **visão de time**.

## Público-alvo

| Perfil | Uso |
|--------|-----|
| **Organizações de esports** | Gestão completa de rosters, scouting global |
| **Analistas de times** | Análise de sinergia, comparação entre jogadores |
| **Coaches profissionais** | Monitoramento de rosters competitivos |
| **Coaches de SoloQ** | Acompanhamento de jogadores em treinamento |

## Diferencial

Enquanto ferramentas atuais entregam **dados crus**, o DraftVision entrega:

- ✅ **Análise estratégica** com insights automáticos
- ✅ **Scouting** com Hidden Talent Detector
- ✅ **Visão de time** e análise de sinergia
- ✅ **Análise de draft** e champion pool coletiva

## Planos

| Plano | Jogadores | Foco |
|-------|-----------|------|
| **Solo Coach** | até 10 | Perfil de jogador, evolução de performance |
| **Team Analyst** | até 50 | Múltiplos times, análise de sinergia |
| **Organization** | ilimitado | Scouting global, API, relatórios avançados |

## Stack técnica

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python, FastAPI, pandas, Redis |
| **Frontend** | Next.js, Tailwind CSS, Chart.js |
| **Banco** | PostgreSQL |
| **Cache** | Redis (obrigatório — API Riot tem rate limit) |

## Estrutura do projeto

```
draftvision/
├── app/
│   ├── api/               # Backend FastAPI
│   │   ├── api/
│   │   │   ├── riot/      # Integração Riot API
│   │   │   ├── players/   # Módulo de jogadores
│   │   │   ├── matches/   # Processamento de partidas
│   │   │   ├── teams/     # Sistema de times
│   │   │   ├── analytics/ # Análise e insights
│   │   │   └── scouting/  # Scouting e Hidden Talent
│   │   └── tests/
│   └── web/               # Frontend Next.js
│       ├── app/
│       │   ├── dashboard/ # Visão geral
│       │   ├── players/   # Perfis de jogadores
│       │   ├── teams/     # Gestão de times
│       │   ├── draft/     # Análise de draft
│       │   └── reports/   # Relatórios
│       └── components/
├── docs/                  # Documentação
└── .github/workflows/     # CI/CD
```

## Começando

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- pnpm
- PostgreSQL 15+
- Redis 7+
- Chave da [Riot Developer API](https://developer.riotgames.com/)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/sthevan027/DraftVision.git
cd DraftVision

# Backend
cd app/api
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env      # Configure suas variáveis

# Frontend
cd ../web
pnpm install
cp .env.example .env.local
```

### Executando

```bash
# Terminal 1 - Redis (obrigatório)
redis-server

# Terminal 2 - Backend
cd app/api && uvicorn main:app --reload --port 8000

# Terminal 3 - Frontend
cd app/web && pnpm dev
```

## Documentação

- [Visão do produto](./docs/PRODUCT_VISION.md)
- [Arquitetura](./docs/ARCHITECTURE.md)
- [Modelo de negócio](./docs/BUSINESS_MODEL.md)
- [Banco de dados](./docs/DATABASE.md)
- [API Riot](./docs/API_RIOT.md)
- [Algoritmos](./docs/ALGORITHMS.md)
- [Worker](./docs/WORKER.md)
- [Roadmap](./docs/ROADMAP.md)
- [Desenvolvimento](./docs/DEVELOPMENT.md)
- [Contribuindo](./docs/CONTRIBUTING.md)

## Design

- [Dashboard](./design/dashboard-design.json) — cores, layout, widgets
- [Logo](./design/logo-design.json) — identidade visual

## Licença

MIT © Sthevan Santos
