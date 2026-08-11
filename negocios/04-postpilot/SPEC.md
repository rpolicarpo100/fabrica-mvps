# SPEC — PostPilot (`postpilot`)
- **Inspiração:** StoryShort.ai / AutoShorts.ai — repurposing de conteúdo ($20k/mês indie)
- **Brief:** Transformar uma peça de conteúdo em variações para X/LinkedIn/Instagram com hooks por plataforma.
- **Formato:** single-file `index.html`, CSS/JS inline, ZERO recursos externos.
- **Execução:** agente.py
- **Critérios de aceitação (smoke test):**
  1. `index.html` válido (<html>/<head>/<body>)
  2. JS syntacticamente válido (node --check)
  3. Sem `src`/`href` http(s) externo
  4. Interatividade presente (event listeners / localStorage)
