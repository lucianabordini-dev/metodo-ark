# {nome-da-feature} — Tasks

**Spec**: `.specs/features/{nome}/spec.md`
**Regra de paralelismo**: paralelo só entre domínios diferentes. Mesmo domínio, sequencial —
salvo quando comprovadamente não tocam os mesmos arquivos.
**Commit**: um commit atômico por task. Nunca agrupar, nunca incluir mudança "de passagem".

---

| # | Domínio | Task | Depende de | AC que atende | Commit |
|---|---|---|---|---|---|
| T1 | banco | | — | A1 | |
| T2 | back-end | | T1 | A1, A2 | |
| T3 | front-end | | T2 | A3 | |

Domínios: `banco` · `back-end` · `front-end` · `regra de negócio` · `arquitetura` · `infra`

---

## Detalhe por task

### T1 — {título}
**Domínio**: banco
**Entrega**: o que existe depois desta task que não existia antes
**Arquivos**: 
**Pronto quando**: (o comando que prova, com o resultado esperado)
