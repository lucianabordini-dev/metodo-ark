# Como executar uma iniciativa

Regra do método neste projeto. Precede conveniência.

## 1. Antes de qualquer coisa: qual é o cenário?

| Cenário | Kit obrigatório |
|---|---|
| Produto do zero | Spec + Arquitetura + Tasks + Validação |
| Feature que toca arquitetura ou domínio | Spec + Arquitetura + Tasks + Validação |
| Feature dentro do padrão existente | Spec + Tasks + Validação |
| Refactor | Arquitetura + Tasks + Validação (asserts intocados) |
| Bug / ajuste pontual | Task + Validação |
| Spike | Pergunta + prazo + resposta escrita |

Cenário declarado no topo da spec. Não declarar é escolher o kit mais leve por omissão.

**Válvula de segurança:** mesmo com as tasks puladas, a execução começa listando os passos.
Mais de cinco passos, ou dependência entre eles, ou mais de um domínio → pare e crie
`tasks.md`. O cenário foi classificado leve demais.

## 2. A pasta da feature

`.specs/features/{nome-em-kebab-case}/` — criada no início, movida para `archive/` no fim.
Nunca trabalhar fora dela.

## 3. Antes de escrever a spec, ler

- `memory/produto.md` — o que é este produto
- `memory/estrutura.md` — onde as coisas moram
- `memory/domain-model.md` — entidades e estados vigentes
- `memory/decisoes.md` — o que já foi decidido e não se rediscute
- `AGENTS.md` — as regras não-negociáveis do código

Não ler `origem/` como requisito vigente. É histórico.

## 3b. Gates que não dependem de memória

| Quando | Comando |
|---|---|
| Antes de confirmar a spec | `python3 <skill-dir>/scripts/valida_spec.py <feature>` |
| Antes de apresentar as tasks | `python3 <skill-dir>/scripts/valida_tasks.py <feature>` |
| A cada commit | `python3 <skill-dir>/scripts/valida_commit.py --message "<msg>"` |
| Antes de declarar pronta | `python3 <skill-dir>/scripts/valida_encerramento.py <feature>` |

Saída diferente de zero = PARAR e corrigir.

## 4. Execução

- Uma task por commit, atômico.
- Paralelo só entre domínios diferentes.
- Task que revela algo não previsto na spec **para** e volta para a spec. Não improvisa.
- Decisão tomada durante a execução vai para `decisoes.md` — não fica no chat.

## 5. Validação

Sub-agente independente. **O verificador nunca conserta**: nomeia o gap, um implementador
fecha, o verificador re-verifica.

## 6. Encerramento

Nesta ordem:
1. `produto.md` e `estrutura.md`, se mudaram
2. `domain-model.md`, se entrou entidade, estado ou relação
3. `decisoes.md` — decisões do caminho + itens que só valem no deploy
4. Lições via `licoes.py registrar`; promover as confirmadas com `licoes.py promover`
5. Mover a feature para `archive/`

Conhecimento só se escreve **depois** do julgamento. Antes disso, documento vira depósito
de tentativa.
