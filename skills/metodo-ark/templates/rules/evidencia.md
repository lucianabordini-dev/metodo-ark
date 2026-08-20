# Formato de evidência

O que conta como prova neste projeto. Vale para toda validação.

## Hierarquia

1. **Comando executado pelo verificador, com a saída.** `33 passed (2.1m)` — rodado por ele,
   não relatado pelo autor.
2. **Assert ancorado em `file:line` observando o outcome definido na spec.** O valor assertado
   é o valor que a spec declara.
3. **Sensor de discriminação.** Mutação no código, uma por vez, e o teste tem que morrer.
4. **Verificação documental** para mudança docs-only, com `git show --stat` provando zero runtime.
5. **Confirmação visual**, só quando o outcome não é observável por assert — e declarada como tal.

## O que nunca conta

- Relato do agente sobre o próprio trabalho ("implementei conforme a spec")
- "Gate verde" sem nome de comando e sem número
- Cobertura como percentual agregado
- Evidência herdada sem o diff que prova que o runtime não mudou

## Profundidade do sensor

| Nível | Quando | Sensor |
|---|---|---|
| Crítico | Pagamento, auth, dado sensível, migration, contenção, invariante declarada | Obrigatório, uma mutação por AC discriminante |
| Padrão | Feature normal | Recomendado, ao menos uma no AC central |
| Baixo | Copy, estilo, documentação | Dispensado |

## Honestidade

- **Evidência parcial é gap nomeado, não PASS com asterisco.**
- **Divergência de precisão se registra, não se apaga.** Provou a mesma propriedade com valores
  diferentes dos do exemplo da spec? Fica anotado.
- **Teste que passa igual com o código quebrado é evidência vazia.** O sensor é a única forma
  de descobrir isso.
