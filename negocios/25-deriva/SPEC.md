# SPEC — 25 Deriva

**Modelo validado:** Prelint — 🥇 #1 Product of the Day (29/07/2026, Product Hunt)
**Categoria:** DevTools / QA de intenção ("economia dos agentes de IA")

## Problema
Equipas usam agentes de IA para gerar código em massa. O produto "deriva" da spec
sem ninguém notar: requisitos ficam por implementar ou saem diferentes.

## MVP
- Input: spec (um requisito por linha) + descrição do construído
- Motor de overlap lexical (stopwords PT, raízes ≥4 letras)
- Saída: % de deriva em anel concênico + checklist ✅🟡❌ por requisito
- Chips com as palavras-chave em falta por requisito
- Histórico local (localStorage), apagável item a item

## Monetização (na vida real)
- SaaS por equipa ($19-49/dev/mês), integração CI; Stripe Payment Links para começar

## Limitações honestas
Overlap lexical ≠ compreensão semântica. Sem LLM, é um triagista, não um revisor.
