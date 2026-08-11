# SPEC — Clica (`18-clica`)
- **Inspiração:** YourSitee (PH top ago-2026) — "faz o teu bio link valer o clique"; IG caption links com cap (Metricool 2026)
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Inputs: @handle, nome, frase de bio, tema (4 gradientes), até 6 links (título+URL, add/remove)
  2. Preview em tempo real da página
  3. Exportar `bio.html` — ficheiro single-file com tudo inline, pronto a alojar em qualquer lado (GitHub Pages, Netlify, servidor próprio)
  4. URLs normalizados (auto https://), rel="noopener", localStorage
- **Critérios de aceitação:** smoke.py verde.
