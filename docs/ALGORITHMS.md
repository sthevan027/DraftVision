# Algoritmos e Métricas

## PlayerScore

Score composto de 0 a 100 que resume a performance do jogador.

### Fórmula

```
PlayerScore =
  (KDA * 0.25) +
  (Winrate * 0.25) +
  (Farm/min * 0.15) +
  (Vision Score * 0.15) +
  (Damage * 0.10) +
  (Consistency * 0.10)
```

### Pesos

| Métrica | Peso | Descrição |
|---------|------|-----------|
| KDA | 25% | Proporção kills+assists/deaths |
| Winrate | 25% | Taxa de vitória (0–100) |
| Farm/min | 15% | Farm por minuto normalizado |
| Vision Score | 15% | Score de visão normalizado |
| Damage | 10% | Dano médio normalizado |
| Consistency | 10% | Variância das performances |

### Normalização

Cada métrica deve ser normalizada para a escala 0–100 antes de aplicar os pesos, usando percentis ou min-max por elo/região quando aplicável.

## Hidden Talent Detector

Identifica jogadores com métricas acima da média para o elo atual (ex: Gold com damage no top 8%).

- Rank: elo do jogador
- Métricas: comparadas ao percentil do elo
- Hidden Talent Score: combinação de métricas acima da média

## Consistência

Medida da variabilidade de performance (ex: desvio padrão do KDA ou coeficiente de variação). Quanto menor a variância, maior a consistência.
