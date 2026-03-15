# Plano de execução para finalizar o V1 (vertical slice)

## Objetivo do V1
Entregar um fluxo funcional ponta a ponta:

1. **Riot API**: buscar conta/jogador e partidas recentes.
2. **Ingestão**: transformar payload bruto em dados normalizados.
3. **Persistência**: salvar dados em PostgreSQL com cache Redis para reduzir chamadas.
4. **Endpoint de perfil**: expor perfil consolidado com métricas iniciais.

## Escopo do vertical slice

### Em escopo (MVP V1)
- Identificação de jogador por `riot_id` (`gameName` + `tagLine`) ou `puuid`.
- Coleta de últimas **20 partidas ranqueadas**.
- Persistência de:
  - Jogador
  - Partida
  - Estatísticas do jogador por partida
- Cálculo de métricas iniciais:
  - Winrate
  - KDA médio
  - CS/min médio
  - Vision score médio
- Endpoint:
  - `GET /players/{puuid}/profile`

### Fora de escopo (V2+)
- Comparação entre jogadores.
- Gestão completa de times/rosters.
- Scouting e Hidden Talent.
- Análise avançada de draft.

## Arquitetura mínima a implementar (alinhada com docs)

### Backend
- `api/riot/`: cliente HTTP Riot + rate limit + retries simples.
- `api/matches/`: ingestão e normalização das partidas.
- `api/players/`: orquestração de perfil e agregação de métricas.
- `api/analytics/`: funções puras para cálculo de métricas.

### Persistência
- Tabelas mínimas:
  - `players`
  - `matches`
  - `player_match_stats`
- Índices principais:
  - `players.puuid` (único)
  - `matches.match_id` (único)
  - `player_match_stats (player_id, match_id)` (único)

### Cache
- Redis para:
  - Resposta de perfil por `puuid` (TTL curto, ex. 5–15 min)
  - Payload de partidas Riot durante ingestão (TTL curto)

## Contratos de API (V1)

### 1) Sincronizar jogador
- `POST /players/sync`
- Entrada:
```json
{
  "game_name": "Nome",
  "tag_line": "BR1"
}
```
- Saída:
```json
{
  "puuid": "...",
  "matches_synced": 20,
  "status": "ok"
}
```

### 2) Perfil consolidado
- `GET /players/{puuid}/profile`
- Saída:
```json
{
  "player": {
    "puuid": "...",
    "summoner_name": "...",
    "region": "br1"
  },
  "metrics": {
    "matches": 20,
    "winrate": 55.0,
    "avg_kda": 3.2,
    "avg_cs_per_min": 7.1,
    "avg_vision_score": 28.4
  },
  "updated_at": "2026-03-14T00:00:00Z"
}
```

## Plano de implementação por etapas

## Etapa 1 — Fundação de domínio e infraestrutura
- Definir schemas (Pydantic) para jogador, partida e estatísticas.
- Definir modelos/tabelas e camada de repositório.
- Configurar conexão com PostgreSQL e Redis.
- Criar migrations iniciais.

**DoD (Definition of Done):**
- Banco sobe localmente com tabelas criadas.
- Testes de repositório (CRUD mínimo) passando.

## Etapa 2 — Cliente Riot + ingestão
- Implementar cliente Riot com:
  - account-v1
  - summoner-v4
  - match-v5 (lista + detalhe)
- Pipeline de ingestão:
  - Buscar jogador
  - Buscar match IDs
  - Buscar detalhes de cada partida
  - Normalizar e persistir
- Garantir idempotência (reprocessar sem duplicar dados).

**DoD:**
- `POST /players/sync` funcional com persistência real.
- Testes de integração com mocks da Riot passando.

## Etapa 3 — Métricas e endpoint de perfil
- Implementar agregações em `analytics` para winrate/KDA/CS/min/vision.
- Implementar `GET /players/{puuid}/profile`.
- Cache de leitura no Redis para perfil consolidado.

**DoD:**
- Endpoint retorna payload estável com métricas corretas.
- Testes unitários de cálculo + integração do endpoint passando.

## Etapa 4 — Hardening mínimo do V1
- Observabilidade básica (logs de sync e erros Riot).
- Timeouts/retries controlados.
- Tratamento de erros de rate limit (429).
- Documentação de execução local e fluxo V1.

**DoD:**
- Execução local reproduzível fim a fim.
- Check de qualidade (lint + testes) passando dentro do possível do ambiente.

## Plano de testes obrigatório por etapa

### Unitários
- Cálculo de métricas em `analytics`.
- Conversão/normalização de payload Riot.
- Regras de idempotência na camada de serviço.

### Integração
- Repositórios com banco de teste.
- `POST /players/sync` com mock da Riot.
- `GET /players/{puuid}/profile` com dados persistidos.

### Contrato/API
- Validação de schema de resposta dos endpoints V1.
- Casos de erro: jogador não encontrado, rate limit, sem partidas.

## Critérios de pronto do V1
- Fluxo completo: Riot → ingestão → persistência → perfil consolidado.
- Cobertura mínima dos casos críticos de negócio.
- Endpoint de perfil estável para consumo do frontend.
- Documentação de operação local atualizada.

## Sequenciamento sugerido (2 semanas)
- **Dia 1–3**: Etapa 1.
- **Dia 4–7**: Etapa 2.
- **Dia 8–10**: Etapa 3.
- **Dia 11–14**: Etapa 4 + estabilização.

## Riscos e mitigação
- **Rate limit da Riot** → cache agressivo + backoff/retry.
- **Inconsistência de dados de partida** → normalização com validação rígida.
- **Crescimento de tempo de sync** → limitar janela inicial (20 partidas) e paginação gradual.
