# SPEC — ProvaFogo (`11-provafogo`)
- **Inspiração:** Replay QA (PH jul-2026) — "diz-te o que está partido antes dos utilizadores"
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Colar HTML → auditoria QA/a11y com DOMParser: links internos quebrados, destinos vazios, IDs duplicados, imgs sem alt/alt vazio, botões sem rótulo, campos sem label, _blank sem noopener, lang/viewport/title, tabelas sem th, autoplay, CLS (imgs sem dimensões), hierarquia de headings, excesso de estilos inline
  2. Score de risco 0–100 com severidades (crítico/aviso/refinamento) e contagens
  3. Cada achado com correção concreta; re-teste após corrigir
- **Critérios de aceitação:** smoke.py verde.
