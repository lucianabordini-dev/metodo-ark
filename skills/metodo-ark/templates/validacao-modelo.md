# {nome-da-feature} — Validação

**Data**: AAAA-MM-DD
**Spec**: `.specs/features/{nome}/spec.md`
**Diff range**: `abc1234..def5678` (N commits)
**Verificador**: sub-agente independente · autor ≠ verificador · evidência ou zero
**Veredito**: PASS ✅ | FAIL ❌ — N/N ACs

> O verificador NÃO conserta. Gap encontrado é gap nomeado; um implementador fecha e
> o verificador re-verifica numa segunda iteração.

---

## Task completion
T1..Tn conferidas contra `git log {range}` — cada task com seu commit.

## Evidência fresca, executada pelo verificador
| Comando | Resultado |
|---|---|
| `<comando exato>` | `N passed (tempo)` |

> Relato do autor não conta. Comando sem saída não conta. "Gate verde" sem número não conta.

## Critérios de aceite, ancorados na spec
| AC | Outcome definido na spec | Evidência (`file:line` + assert) | Result |
|---|---|---|---|
| A1 | | | ✅ |

## Sensor de discriminação
> Quebrar o código de propósito, uma mutação por vez, e o teste tem que morrer.
> Obrigatório em caminho crítico (pagamento, auth, dado sensível, migration, contenção,
> invariante declarada). Recomendado no AC central de feature normal. Dispensado em copy e estilo.

| # | Mutação (`arquivo:alvo`) | Teste executado | Resultado |
|---|---|---|---|
| 1 | | | ✅ KILLED |

**Restauração**: todas as mutações descartadas; `git status` sem resíduo.

## Qualidade
| Princípio | Status |
|---|---|
| Sem nada além do escopo (diff = superfícies das tasks) | |
| Asserts existentes não enfraquecidos | |
| Valores assertados = valores da spec | |

## Observações de precisão (não-bloqueantes)
> Divergência se registra, não se apaga. AC provado por composição entra aqui.

## Gaps
> Vazia num PASS. Cada gap: o que falta, onde, e o que decidir.

## Conhecimento a atualizar
- [ ] `memory/produto.md` / `estrutura.md` / `domain-model.md`
- [ ] `memory/decisoes.md` — decisões e itens de produção
- [ ] `memory/lessons.md` — lições; promover as de 2ª ocorrência
- [ ] Mover `features/{nome}/` para `archive/`
