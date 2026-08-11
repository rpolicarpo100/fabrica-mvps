# 🚀 Publicar — GitHub Pages + Render

O site já está publicado em **duas plataformas grátis** (custo 0):

| Plataforma | URL | Estado |
|------------|-----|--------|
| GitHub Pages | https://rpolicarpo100.github.io/fabrica-mvps/ | ✅ no ar |
| Render | https://fabrica-mvps.onrender.com | ⏳ ativar no dashboard |

## Render (Blueprint — 3 cliques)

O ficheiro `render.yaml` na raiz já define tudo. Para ativar:

1. Vai a <https://render.com> → regista-te **com a conta GitHub** (rpolicarpo100)
2. Autoriza o acesso ao repositório `fabrica-mvps`
3. Dashboard → **New +** → **Blueprint** → seleciona `rpolicarpo100/fabrica-mvps`

O Render lê o `render.yaml`, cria o Static Site e publica em `fabrica-mvps.onrender.com`.
Cada `git push` para `main` atualiza o site sozinho (auto-deploy).

⚠️ Notas do tier grátis (2026): ~5 GB/mês de banda no workspace Hobby; pode pedir cartão
só como verificação anti-abuso (não cobra dentro dos limites). Sem hibernação para
sites estáticos.

---

## Notas GitHub Pages

## Opção A — Fazes tu o push (recomendado, mais seguro)

1. Cria um repositório **vazio** em <https://github.com/new>
   - Nome sugerido: `fabrica-mvps`
   - Visibilidade: **Público** (Pages grátis)
   - ⚠️ Não adiciones README, licença nem .gitignore (já existem aqui)

2. Na pasta do projeto, corre:

```bash
git remote add origin https://github.com/rpolicarpo100/fabrica-mvps.git
git push -u origin main
```

3. O workflow `.github/workflows/pages.yml` corre automaticamente no primeiro push
   e publica o portal em `https://rpolicarpo100.github.io/fabrica-mvps/`
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
