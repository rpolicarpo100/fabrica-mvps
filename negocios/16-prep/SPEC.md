# SPEC — Prep (`prep`)
- **Inspiração:** LeetDesign — entrevistador de system design
- **Brief:** Banco de casos system design PT + esboço + resposta modelo + rubrica
- **Formato:** single-file `index.html`, CSS/JS inline, ZERO recursos externos.
- **Execução:** agente.py
- **Critérios de aceitação (smoke test):**
  1. `index.html` válido (<html>/<head>/<body>)
  2. JS syntacticamente válido (node --check)
  3. Sem `src`/`href` http(s) externo
  4. Interatividade presente (event listeners / localStorage)
