# SPEC — Recupera (`23-recupera`)
- **Inspiração:** Dunning/payment-recovery (classe Churnkey, $20K–$360K ARR — flowjam 2026)
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Calculadora: subscritores, preço médio, churn %, taxa de falha → € falhado/mês, recuperável (benchmark 55%), ARR salvo
  2. Sequência de 4 emails de dunning PT (dia 0/2/5/7) com escalada de tom e placeholders {nome}/{valor}/{link}
  3. Copiar por email; nota técnica sobre smart retries; localStorage
- **Critérios de aceitação:** smoke.py verde.
