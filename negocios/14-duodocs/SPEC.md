# SPEC — DuoDocs (`14-duodocs`)
- **Inspiração:** DocsAlot (PH #1 do dia 05-07-2026) — "documentação que serve humanos e sistemas de IA"
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Nome do produto + notas livres (linhas) com sintaxe simples: `Secção: texto`, `- bullet`, `Pergunta? | Resposta`
  2. Saída 1 — Doc para humanos: estrutura tipo README (intro, funcionalidades, como começar, FAQ) renderizada + MD
  3. Saída 2 — llms.txt: ficheiro estruturado para agentes/LLMs (contexto, entradas/saídas, limites, tom)
  4. Copiar/descarregar cada saída; tabs; exemplo; localStorage
- **Critérios de aceitação:** smoke.py verde.
