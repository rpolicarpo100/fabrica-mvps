# 🚀 Publicar no GitHub

O repositório já está preparado localmente (commit inicial feito). Falta apenas o push.

## Opção A — Fazes tu o push (recomendado, mais seguro)

1. Cria um repositório **vazio** em <https://github.com/new>
   - Nome sugerido: `fabrica-mvps`
   - Visibilidade: **Público** (Pages grátis)
   - ⚠️ Não adiciones README, licença nem .gitignore (já existem aqui)

2. Na pasta do projeto, corre:

```bash
git remote add origin https://github.com/TEU-UTILIZADOR/fabrica-mvps.git
git push -u origin main
```

3. O workflow `.github/workflows/pages.yml` corre automaticamente no primeiro push
   e publica o portal em `https://TEU-UTILIZADOR.github.io/fabrica-mvps/`
   (se necessário: Settings → Pages → Source: **GitHub Actions**)

## Opção B — Eu faço o push (com token)

1. Se usares **token classic**: <https://github.com/settings/tokens/new> com scopes `repo` + `workflow`.
   Se usares **fine-grained**: <https://github.com/settings/personal-access-tokens/new>
   — cria primeiro o repo vazio em github.com/new, depois um token só para esse repo
   com permissões **Contents: Read and write** + **Workflows: Read and write**.

2. Cola o token aqui no chat e diz-me o nome do repositório.

3. Eu faço o push (o token é usado apenas em linha de comando, nunca gravado em ficheiros)
   e podes revogá-lo de seguida em 10 segundos.

## Notas

- Repo **privado**: GitHub Pages só funciona com plano Pro. O código fica privado, sem site público.
- Nenhum token/chave é gravado em ficheiros deste projeto (ver `.gitignore`).
