# Nomenclatura

## Pastas e arquivos do método

| Coisa | Formato | Exemplo |
|---|---|---|
| Pasta de feature | kebab-case, sem prefixo de data | `checkout-multi-produto/` |
| Documentos da feature | fixos | `spec.md` `arquitetura.md` `tasks.md` `validation.md` |
| Documentos de origem | fixos | `mvp-scope.md` `fundacao.md` `prd.md` `base-tecnica.md` |

## Identificadores

| Tipo | Prefixo | Exemplo |
|---|---|---|
| Regra de validação | `RN-V` | RN-V01 |
| Regra de invariante | `RN-I` | RN-I01 |
| Regra de transição | `RN-T` | RN-T01 |
| Regra de autorização | `RN-A` | RN-A01 |
| Decisão arquitetural | `D-` | D-014 |
| Lição | `L-` | L-007 |
| Task | `T` | T3 |
| Critério de aceite | letra + número | A1, B2 |

**Identificador não se renumera e não se reutiliza.** Regra revogada fica com a marca de
revogada, a data e o motivo. Apagar uma regra é apagar o porquê de tudo que foi construído
em cima dela.

## Código

Definido em `AGENTS.md`, não aqui. Este arquivo governa o método; aquele governa o código.
