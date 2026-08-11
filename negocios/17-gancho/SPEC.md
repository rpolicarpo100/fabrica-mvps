# SPEC — Gancho (`17-gancho`)
- **Inspiração:** Packaging tools YouTube 2026 (Pikzels ~$25K MRR, ThumbnailTest, OverseerOS)
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Cola o título/hook → score CTR 0-100 por heurísticas: comprimento por plataforma (YT 50-70, X/IG 100-150), números, poder/curiosidade PT, pergunta, parênteses, ano, especificidade, caps abuse, emojis
  2. Deteção de "clickbait vazio" (promessa sem especificidade) com aviso
  3. Gerador de 5 variantes a partir do tema (numérica, como-fazer, contrária, pergunta, guia)
  4. Copiar variante; localStorage; exemplo
- **Critérios de aceitação:** smoke.py verde.
