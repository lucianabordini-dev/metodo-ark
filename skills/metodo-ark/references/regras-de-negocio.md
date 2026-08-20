# Regras de Negócio
### O pilar menos óbvio e mais valioso do Método Ark
*v1 — agosto de 2026*

---

## Por que este documento existe

A arquitetura de um produto não nasce da stack. Nasce das regras de negócio.

Quem pula a extração de regras e vai direto para o código — ou direto para o prompt — constrói um software que não reflete a realidade do negócio. E descobre isso em produção, que é o lugar mais caro possível para descobrir.

A parte difícil não é escrever a regra depois de conhecê-la. É **ouvi-la**. Ela quase nunca aparece como regra na fala de quem vive o problema: aparece como reclamação, como exceção, como "ah, mas quando é X a gente faz diferente". Este documento ensina a reconhecer os quatro formatos em que ela se esconde.

---

## Os quatro tipos

Toda regra de negócio cai em um destes quatro. Se não cair, provavelmente não é regra — é preferência, ou é feature disfarçada.

---

### 1. Validação — *a condição para algo poder existir ou mudar*

**O que é.** Uma verificação que acontece **no momento em que alguém tenta fazer alguma coisa**. Se a condição não for satisfeita, a coisa não acontece. É a regra que diz "não, assim não pode".

**Como você reconhece na fala de quem vive o problema.** Procure por *só pode se*, *não deixa*, *tem que ter*, *precisa preencher*, *aí o sistema não aceita*, *daí a gente barra*. É o tipo mais fácil de ouvir, porque as pessoas descrevem validação como se fosse óbvio — e é justamente por parecer óbvio que ela não é escrita.

> *"Carga não precisa de data, mas sem prioridade eu não consigo saber o que provisionar primeiro."*
> → Carga exige valor estimado e prioridade, e não exige data. Carga sem prioridade não pode ser provisionada.

> *"Já aconteceu de eu começar a gravar e o disco encher no minuto 40."*
> → Espaço livre em disco é verificado antes de iniciar; abaixo do limiar, a gravação não começa.

**O que vira no código.** Guard no início da função, validação de payload na API, `check constraint` quando dá para expressar em banco, validação de formulário no front. A validação de front é conveniência; **a que vale é a do servidor** — a do front pode ser burlada com o DevTools aberto.

**A pergunta que revela validações escondidas:** *"o que aconteceria se alguém tentasse fazer isso pela metade?"*

---

### 2. Invariante — *o que é sempre verdade, o tempo todo*

**O que é.** Uma afirmação sobre o sistema que **não pode ser falsa em nenhum momento**, por nenhum caminho. Não é uma verificação num ponto: é uma propriedade que precisa se sustentar depois de qualquer operação possível.

A diferença para a validação é temporal, e é a que mais confunde. **Validação acontece uma vez, na entrada. Invariante vale para sempre, em toda parte.** Uma validação mal escrita deixa um dado ruim entrar. Uma invariante violada significa que o sistema está mentindo — e sistemas que mentem produzem decisões erradas silenciosamente.

**Como você reconhece na fala.** Procure por *nunca*, *sempre*, *em hipótese nenhuma*, *não pode acontecer de*, *isso jamais*. Vem quase sempre com emoção — é o tipo de regra que as pessoas dizem em voz mais alta, porque costuma ter uma cicatriz atrás.

> *"O saldo da conta parece suficiente, mas parte daquilo já tem dono."*
> → Livre = Saldo − Compromissos até o próximo recebimento − Reserva − Provisionado. Saldo bruto nunca é apresentado como disponível.

> *"Perder uma hora de gravação por causa de um crash é inaceitável."*
> → Os arquivos de captura originais são imutáveis após o encerramento; nenhuma operação de edição os altera ou destrói.

> *"O cliente não pode mudar o preço."*
> → O servidor é a única autoridade de preço. O cliente exibe preço, nunca o dita.

**O que vira no código.** `unique`/`foreign key`/`not null` e constraints compostas em banco, RLS, testes de invariância (a classe de teste que tenta violar a propriedade por vários caminhos), e o padrão de **produtor único**: quando uma invariante diz que algo tem uma fonte só, o código materializa isso com um arquivo único autorizado a fazer aquilo, mais um verificador que falha o gate se alguém escrever fora dele.

**A pergunta que revela invariantes escondidas:** *"qual é a coisa que, se acontecesse, seria um desastre — não um bug chato, um desastre?"*

---

### 3. Transição de estado — *quando e como uma coisa muda de situação*

**O que é.** Coisas importantes de um negócio não são só dados: elas têm **situações** e um caminho permitido entre elas. Um recebimento é previsto, depois confirmado, depois recebido — e pode atrasar no meio, mas não pula de previsto para recebido sem passar por lugar nenhum.

Modelar isso explicitamente é o que evita a classe de bug mais cara que existe: o sistema num estado que ninguém previu. Pedido pago e cancelado ao mesmo tempo. Assinatura ativa sem cobrança. Gravação finalizada com arquivo aberto.

**Como você reconhece na fala.** Procure por *aí vira*, *depois que*, *quando ele passa para*, *fica pendente até*, *só liberamos depois de*, *se der errado volta para*. Também aparece como substantivo de estado: *pendente*, *aprovado*, *em análise*, *cancelado*. **Toda vez que uma palavra dessas aparece, existe uma máquina de estado não escrita.**

> *"O freela pode atrasar, mas quando cai eu preciso saber que era aquele."*
> → Recebimento: `Previsto → Confirmado → Recebido` · `Previsto → Atrasado → Recebido` · `Previsto → Cancelado`

> *"Se o projeto está renderizando, não dá para mexer nele."*
> → Projeto: `rascunho → editando → renderizando → exportado`. Projeto em `renderizando` não pode ser editado nem deletado.

**O que vira no código.** Enum de estado no banco (nunca string livre), uma função única de transição que valida a origem antes de gravar o destino, e a regra de ouro do domínio: **estado não se atribui, se transiciona**. Cada transição costuma carregar efeito colateral — e a ordem entre gravar o estado e disparar o efeito é decisão arquitetural, não detalhe.

**A pergunta que revela transições escondidas:** *"desenha para mim o caminho dessa coisa, do nascimento até sumir — e onde ele pode dar errado no meio?"*

---

### 4. Autorização — *quem pode o quê*

**O que é.** A regra que separa quem pode fazer uma coisa de quem não pode. Nem sempre é papel de usuário: pode ser plano contratado, estado da licença, propriedade do dado, ou momento no fluxo.

É o tipo mais perigoso de deixar implícito, porque a falha não aparece como erro. Aparece como uma pessoa vendo o dado de outra — e, quando aparece, já aconteceu.

**Como você reconhece na fala.** Procure por *só o gerente*, *o cliente não pode ver*, *isso é do plano X*, *depois que assina libera*, *cada um vê só o seu*. Repare que quase sempre vem como **descrição de organograma**, não como regra de software — e é trabalho de quem extrai fazer essa tradução.

> *"Sem licença ainda dá para usar, mas o vídeo sai com marca d'água."*
> → Sem licença: gravação e edição livres, export com marca d'água. O funil é o output, não o tempo.

> *"São meus dados financeiros, não quero isso num servidor de ninguém."*
> → Usuário único, sem papéis. A regra que sobra é posse do dado: dados são locais e não trafegam para terceiros.

**O que vira no código.** Policies e RLS no banco (a camada que não se esquece), middleware de rota, checagem por tier no catálogo de planos, escopo de token. **Autorização no front é decoração** — ela esconde o botão, não protege o endpoint.

**A pergunta que revela autorizações escondidas:** *"quem NÃO pode ver isso? e o que acontece se essa pessoa souber o link direto?"*

---

## Como escrever uma regra

Regra que não é rastreável até o código é intenção, não fonte. É isso que faz "spec-as-source" ser verdade e não slogan.

**Formato canônico:**

```
RN-{TIPO}{NÚMERO} — {enunciado em uma frase, em linguagem de negócio}
  Origem:      onde essa regra apareceu (entrevista, incidente, decisão, lei)
  Implementada: caminho:linha do que a cobra
  Provada por:  o teste ou o gate que falha se ela for violada
```

Prefixos: `RN-V` validação · `RN-I` invariante · `RN-T` transição · `RN-A` autorização.

Exemplo completo:

```
RN-I01 — O saldo bruto nunca é apresentado como disponível. O que a pessoa vê é
         o Livre: saldo menos compromissos até o próximo recebimento, menos
         reserva, menos o que já está provisionado em cargas.
  Origem:       perrengue documentado — dinheiro acabou antes do recebimento
                porque o saldo na conta parecia suficiente
  Implementada: shared/finance/livre.ts
  Provada por:  test/livre.spec.ts — mutação que remove a subtração da reserva
                mata o teste
```

**Três regras sobre escrever regra:**

1. **Uma frase, em linguagem de negócio.** Se precisar de termo técnico para enunciar, ainda não é regra de negócio — é decisão de implementação, e vai para `decisoes.md`.
2. **Numerada e imutável.** Regra não se renumera. Regra revogada fica com a marca de revogada, a data e o motivo — apagar uma regra é apagar o porquê de tudo que foi construído em cima dela.
3. **Sem "deveria".** Regra é indicativo, não conselho: *"o servidor calcula o preço"*, nunca *"o servidor deveria calcular o preço"*.

---

## Como caçar regras numa conversa

Vale igualmente para entrevistar outra pessoa e para se entrevistar.

**Peça o passo a passo, não a opinião.** *"Me mostra como você faz isso hoje, do começo ao fim"* rende dez vezes mais que *"o que o sistema precisa ter?"*. Pessoas descrevem processo com precisão e especificam features com imprecisão.

**Cace a exceção.** Toda frase que começa com *"normalmente"* tem uma regra escondida logo atrás. Pergunte *"e quando não é normalmente?"*.

**Cace a cicatriz.** *"Já deu problema alguma vez?"* é a pergunta que produz invariantes. Invariante quase sempre nasce de um desastre.

**Cace o manual.** O que a pessoa faz na mão — a planilha paralela, o post-it, o conferir duas vezes — é onde o sistema atual não cobre a regra. É ouro.

**Não pergunte se pagariam.** Isso é validação de mercado, e é assunto de MVP Scope, não de extração de regra.

---

## Erros comuns

| Erro | Como se manifesta | Correção |
|---|---|---|
| Confundir validação com invariante | A regra é checada na entrada e violada por outro caminho depois | Perguntar: isso é verdade *sempre*, ou só neste momento? |
| Feature disfarçada de regra | "O sistema precisa ter um dashboard" | Regra descreve o negócio, não a interface |
| Regra sem origem | Ninguém lembra por que existe, ninguém ousa remover | Origem é campo obrigatório |
| Regra técnica demais para o cliente ler | Quem vive o problema não consegue confirmar se está certa | Reescrever em linguagem de negócio; o técnico vai para a implementação |
| Estado como string livre | `status = "aprovadoo"` em produção | Enum + função única de transição |
| Autorização só no front | Endpoint aberto para quem souber a URL | Toda autorização tem versão de servidor |

---

## O caminho da regra até a arquitetura

| Nasce | É formalizada | Vira |
|---|---|---|
| **Fundação** — extraída em linguagem de negócio | **PRD** — numerada e tipada | Validação → guards e validação de API |
| | | Invariante → constraints, RLS, testes de invariância, produtor único |
| | | Transição → **Domain Model**: máquina de estado e ciclo de vida |
| | | Autorização → policies, middleware, tiers, escopo de token |

E, a partir daí, cada regra aparece de novo em toda spec de feature que a toca — como restrição vigente, não como novidade. É assim que uma regra escrita uma vez governa o produto inteiro.
