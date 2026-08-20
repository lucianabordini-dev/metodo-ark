# Publicar

## 1. Tornar o repositório público

Settings → General → Danger Zone → Change visibility → Public.

**Enquanto estiver privado, nenhum comando de instalação funciona** — nem `npx`, nem `git clone`,
nem `curl`. É o primeiro passo, não o último.

## 2. Publicar no npm

```bash
npm login
npm publish --access public
```

O nome `metodo-ark` estava livre no npm em agosto de 2026. A partir daí:

```bash
npx metodo-ark install
```

`files` no `package.json` limita o tarball a `bin/`, `skills/`, `README.md` e `LICENSE` —
confira antes com `npm pack --dry-run`.

## 3. Versionar

`version` no `package.json` acompanha a versão do método. Mudança no `SKILL.md` ou nas
referências = versão nova publicada, senão quem instalou fica na antiga sem saber.

```bash
npm version minor && npm publish && git push --follow-tags
```

E crie uma Release no GitHub com o mesmo número — é o que dá para apontar quando alguém
perguntar "o que mudou".

## 4. Antes do primeiro commit público

- [ ] Busca no INPI por conflito de marca com "Método Ark" no nicho — repo público com o nome
      no título é uso público datado. Ajuda a provar anterioridade, e também é o momento em que
      alguém pode reagir.
- [ ] Conferir que nenhum documento público cita cliente, empregador ou dado interno:
      `grep -riE "wefoundr|dunno|raccord|arkanum|cliente" skills/`
- [ ] `npm pack --dry-run` e ler a lista de arquivos.
