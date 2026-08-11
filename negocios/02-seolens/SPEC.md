# SPEC — SEOLens (`02-seolens`)
- **Inspiração:** OpenSEO (PH #3 jul-2026) + tendência GEO (Scribble Network)
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Colar HTML → auditoria local (title, meta description, h1, hierarquia H2-H6, alt de imagens, canonical, lang, viewport, OG/Twitter cards, JSON-LD)
  2. Análise de conteúdo: nº palavras, densidade de keywords (stopwords PT), legibilidade simples
  3. Score GEO: FAQ, listas, resposta direta no início, dados citáveis, schema
  4. Score 0-100 por categoria + anéis SVG + recomendações por severidade
  5. Exportar relatório em Markdown (download local)
- **Critérios de aceitação:** smoke.py verde.
