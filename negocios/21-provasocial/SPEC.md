# SPEC — ProvaSocial (`provasocial`)
- **Inspiração:** Senja/Famewall — testemunhos (2026)
- **Brief:** Testemunhos → moderação → Wall of Love exportável
- **Formato:** single-file `index.html`, CSS/JS inline, ZERO recursos externos.
- **Execução:** assistente
- **Critérios de aceitação (smoke test):**
  1. `index.html` válido (<html>/<head>/<body>)
  2. JS syntacticamente válido (node --check)
  3. Sem `src`/`href` http(s) externo
  4. Interatividade presente (event listeners / localStorage)
