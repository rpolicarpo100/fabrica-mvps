# SPEC — LeadForge (`03-leadforge`)
- **Inspiração:** Fuzzy AI (PH #7 jul-2026) — "aquecer prospects antes do outreach"
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Importar leads em CSV (nome,email,empresa,cargo,website,notas) com auto-mapeamento de colunas
  2. Scoring heurístico 0–100 (domínio corporativo, senioridade do cargo, website, email válido, sinais de compra nas notas) → tiers Quente/Morno/Frio
  3. Gerador de primeira mensagem personalizada (email + LinkedIn) por tier, com interpolação de nome/empresa/cargo
  4. Pipeline com estados (Novo→Contactado→Respondeu→Reunião) + persistência localStorage
  5. Dados de exemplo + apagar tudo
- **Critérios de aceitação:** smoke.py verde.
