# Modelagem do Banco de Dados

## Visão geral

O DraftVision usa PostgreSQL para persistir jogadores, partidas, times e relações entre eles. As métricas agregadas (winrate, KDA, farm/min, etc.) são calculadas a partir dos dados de partidas.

## Tabelas

### players

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid | Chave primária |
| puuid | text | PUUID único da Riot |
| riot_id | text | Nome#TAG (ex: faker#KR1) |
| region | text | Região (br1, na1, kr, etc.) |
| rank | text | Elo atual |
| winrate | float | Taxa de vitória (0–1) |
| kda | float | Kills + Assists / Deaths |
| farm_per_min | float | Farm por minuto |
| vision_score | float | Score de visão médio |
| created_at | timestamp | Data de criação |
| updated_at | timestamp | Última atualização |

### matches

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid | Chave primária |
| match_id | text | ID da partida (Riot) |
| duration | int | Duração em segundos |
| created_at | timestamp | Data de criação |

### player_matches

Tabela de associação entre jogadores e partidas, com dados específicos da partida.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| player_id | uuid | FK → players |
| match_id | uuid | FK → matches |
| champion | text | Campeão jogado |
| kills | int | Abates |
| deaths | int | Mortes |
| assists | int | Assistências |
| gold | int | Ouro total |
| damage | int | Dano causado |
| vision_score | int | Score de visão |

### teams

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid | Chave primária |
| name | text | Nome do time |
| created_at | timestamp | Data de criação |

### team_players

Associação entre times e jogadores com role.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| team_id | uuid | FK → teams |
| player_id | uuid | FK → players |
| role | text | Top, Jungle, Mid, ADC, Support |

## Diagrama ER (conceitual)

```
players ──┬──< player_matches >──┬── matches
          │                      │
          └──< team_players >──┬─┘
                               │
teams ─────────────────────────┘
```

## Índices recomendados

- `players(puuid)` — busca por PUUID
- `players(riot_id, region)` — busca por nome
- `player_matches(player_id)` — histórico do jogador
- `player_matches(match_id)` — jogadores da partida
- `matches(match_id)` — partida por ID Riot
