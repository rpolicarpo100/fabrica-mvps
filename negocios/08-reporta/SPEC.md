# SPEC — Reporta (`08-reporta`)
- **Inspiração:** Migma AI (PH jul-2026) — "pergunta ao analista de IA, recebe relatório pronto a partilhar"
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Colar CSV → deteção automática de separador e tipos (numérico, data, categoria)
  2. KPIs: linhas, colunas, % células vazias
  3. Estatísticas por coluna numérica (soma, média, mediana, mín/máx, desvio)
  4. Gráficos SVG inline: barras (top categorias) e linha temporal (por mês)
  5. Insights automáticos em PT (liderança, tendência, melhor período, outliers IQR, qualidade de dados)
  6. Exportar relatório .md e dashboard .html standalone
- **Critérios de aceitação:** smoke.py verde.
