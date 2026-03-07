# Contribuindo com o DraftVision

Obrigado por considerar contribuir. Este documento descreve o fluxo esperado.

## Código de conduta

Seja respeitoso e construtivo em todas as interações.

## Como contribuir

1. **Reportar bugs** – Abra uma issue descrevendo o problema e passos para reproduzir
2. **Sugerir features** – Use issues para discutir ideias antes de implementar
3. **Pull requests** – Correções e novas features são bem-vindas

## Fluxo de trabalho

1. Faça fork do repositório
2. Crie uma branch: `git checkout -b feature/minha-feature` ou `fix/meu-fix`
3. Faça suas alterações
4. Garanta que testes passem e o lint está ok
5. Commit com [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: adiciona comparação de jogadores`
   - `fix: corrige cálculo do PlayerScore`
   - `docs: atualiza README`
6. Push e abra um Pull Request
7. Aguarde review

## Padrões de código

- **Python**: Black (formatação), Ruff (lint)
- **TypeScript/React**: ESLint, Prettier
- **Commits**: Mensagens claras em português ou inglês

## Estrutura de PR

- Título descritivo
- Descrição do que mudou e por quê
- Referência a issues relacionadas, se houver
- Checklist: testes, lint, documentação

## O que priorizar

- Integração com Riot API e cache
- Módulos de análise (PlayerScore, Hidden Talent)
- UX do dashboard e relatórios
- Testes e documentação
