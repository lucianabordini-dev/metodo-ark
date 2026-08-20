# AGENTS.md — {Projeto}

> **Arquivo canônico de regras deste repositório**, no padrão aberto `AGENTS.md`.
> `CLAUDE.md` é um stub que importa este conteúdo. **Regra nova de código entra aqui.**
>
> Regras do **método** (como executar uma spec, formato de evidência, nomenclatura de feature)
> não moram aqui — moram em `.specs/rules/`. Cada regra mora num lugar só.

## Arquitetura em uma frase

{Uma frase. Se não couber numa frase, a arquitetura ainda não foi decidida.}

## Regras transversais (não-negociáveis)

### C-1 — {título curto e imperativo}
O que é proibido, o que fazer no lugar, e onde está a decisão que originou isso.

### C-2 — {título}

## Gates — rodar antes de considerar uma task pronta

| Nível | Quando | Comando |
|---|---|---|
| Quick | unit/typecheck | `` |
| Full | toca fluxo/endpoint | Quick + `` |
| Build | última task da fase | Full + `` |

A gate é determinística: quem decide se o código está correto é o test runner, não
auto-avaliação.

## Invariantes vigentes

### {Invariante em linguagem natural}
Qual arquivo é o produtor único, como se obtém a coisa, e qual verificação falha se alguém
escrever fora dele.

## Padrões de código
- Onde cada coisa mora: `.specs/memory/estrutura.md`
- Nomenclatura de código:
- Tipagem:
- Estilo:

## Branch e commits
- Branch de trabalho:
- **Um commit atômico por task** — nunca agrupar, nunca incluir mudança "de passagem".
- Conventional Commits: `type(scope): descrição`

## Como responder no chat
Objetivo, veredito primeiro, sem preâmbulo e sem auto-resumo. Item técnico entra como
**evidência** do que foi dito (caminho, `file:line`, número de teste), nunca como o argumento.
Concisão nunca corta o que muda a decisão: risco, irreversibilidade, trade-off, o que **não**
foi testado, e falha — sempre relatada com o erro, nunca embrulhada em otimismo.
