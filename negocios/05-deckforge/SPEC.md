# SPEC — DeckForge (`deckforge`)
- **Inspiração:** Gamma — apresentações geradas por IA ($100M ARR)
- **Brief:** Outline de texto → deck de slides HTML navegável.
- **Formato:** single-file `index.html`, CSS/JS inline, ZERO recursos externos.
- **Execução:** agente.py
- **Critérios de aceitação (smoke test):**
  1. `index.html` válido (<html>/<head>/<body>)
  2. JS syntacticamente válido (node --check)
  3. Sem `src`/`href` http(s) externo
  4. Interatividade presente (event listeners / localStorage)
