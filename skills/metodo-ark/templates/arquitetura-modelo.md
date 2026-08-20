# {nome-da-feature} — Arquitetura

**Spec**: `.specs/features/{nome}/spec.md`
**Obrigatória porque**: (produto do zero | toca arquitetura | toca domínio | é refactor)

---

## 1. Decisão em uma frase

## 2. Como fica
Diagrama ou descrição de camadas, fluxo e responsabilidades.

## 3. Regras de negócio → estrutura
| Regra | Tipo | Vira |
|---|---|---|
| RN-x0x | invariante | constraint em `tabela.coluna` |

## 4. Alterações no domínio
- Entidades novas ou alteradas:
- Estados novos e transições:
- Impacto em `memory/domain-model.md`:

## 5. Contratos
Endpoints, payloads, eventos, tipos compartilhados.

## 6. Banco
Migrations, índices, constraints, RLS.

## 7. Segurança
Autorização, dado sensível, o que não pode vazar em log.

## 8. Alternativas descartadas
| Alternativa | Por que não |
|---|---|

## 9. Produtor único
Se alguma invariante exige fonte única (preço, IP do cliente, segredo, estado de circuito):
qual arquivo é o produtor, e qual verificação falha se alguém escrever fora dele.
