# Status atual do projeto (diagnóstico rápido)

## O que já foi feito

### Estrutura e direcionamento
- Repositório organizado com backend (`app/api`), frontend (`app/web`) e documentação de produto/arquitetura.
- Visão de produto, arquitetura, banco, roadmap e guias de desenvolvimento já documentados.

### Backend (implementado)
- API FastAPI inicial criada com metadados da aplicação.
- CORS configurado para consumo local pelo frontend (`http://localhost:3000`).
- Endpoints básicos já funcionais:
  - `GET /` retorna nome e versão da API.
  - `GET /health` retorna status de saúde.
- Testes automatizados básicos para os dois endpoints existentes.

### Frontend (implementado)
- App Next.js inicial configurada.
- Página inicial com branding e descrição da proposta do produto.
- Configuração base de TypeScript, Tailwind e lint.

## O que falta (gap para MVP)

### Funcionalidades de negócio
De acordo com o roadmap, os itens de V1, V2 e V3 ainda estão pendentes, incluindo:
- Integração real com Riot API.
- Perfil de jogador e histórico de partidas.
- Cálculo de métricas (KDA, winrate, farm/min, visão).
- Dashboard inicial com dados.
- Gestão de times e comparação de jogadores.
- Champion pool analysis.
- Scouting automático, Hidden Talent Detector e análise de draft.

### Backend técnico
- Implementar módulos reais sob `api/players`, `api/matches`, `api/teams`, `api/analytics`, `api/scouting` (atualmente apenas placeholders de pacote).
- Definir modelos de dados/persistência e fluxo com PostgreSQL/Redis.
- Adicionar camada de domínio/use cases conforme arquitetura proposta na documentação.

### Frontend técnico
- Criar rotas e componentes de dashboard, players, teams, draft e reports.
- Conectar frontend ao backend por cliente HTTP e tratar estados de loading/erro.
- Incluir visualizações de dados (gráficos/tabelas) além da landing inicial.

### Qualidade e operação
- Expandir suíte de testes (unitários + integração) para módulos de negócio.
- Configurar pipeline CI para lint + testes de backend e frontend em todos os PRs.
- Definir estratégia inicial de migração de banco e seeds.

## Próximos passos sugeridos (ordem prática)
1. Fechar vertical slice de V1: Riot API → ingestão de partidas → persistência → endpoint de perfil.
2. Publicar dashboard inicial consumindo endpoints reais (mesmo com métricas mínimas).
3. Evoluir cobertura de testes junto com cada módulo entregue.
4. Só depois avançar para V2 (times/comparação) e V3 (scouting/draft).
