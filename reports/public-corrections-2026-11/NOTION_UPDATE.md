# Notion update — paste into the task row

**Task:** SoroJá: consolidar planilha de correções do público em achado documentável
**Status:** Not started → **Done** (the finding is drafted; review the PIPE paragraph before using it)
**Why this file exists:** on 2026-11-13 every Notion connector call (search/fetch) returned a server error. Update the row by hand.

## Summary (paste into the page)

Consolidei a planilha de controle "Error Reports Summary V2" (364 linhas, 22/04 a 22/10/2026) num achado documentado.

- **Público:** 43 relatos novos e 8 corroborações, de 13 UFs. 40 relatos são sobre dados: telefone 11, pin no mapa 11, atendimento em outra unidade 6, unidade fechada 5, unidade ausente 4, dados trocados na fonte 2, sem estoque 1.
- **Alcance:** 35 das 2.279 unidades publicadas (1,5%) receberam relato de erro. 17 têm erro confirmado, mais 1 registro ocultado; 16 só têm o relato publicado; 2 estão pendentes.
- **Confirmação:** 18 de 20 relatos verificados se confirmaram (90%).
- **Listas oficiais:** comparando a lista federal com as estaduais em PR, ES, PE e RN, 231 de 285 unidades federais (81%) têm dados diferentes ou não constam da lista estadual.
- **Achado PIPE:** a lista oficial não tem processo de atualização. A verificação comunitária tem alto valor preditivo, mas é voluntária. Proposta: validação contínua e sistemática.

## Where the files are

`reports/public-corrections-2026-11/` in the sos-antiveneno repo. **Not committed**: the folder is local and untracked.

- `ACHADO.md`: the finding in Portuguese, with tables, limits and a paragraph ready for the report or proposal.
- `relatos_publico.csv`, `comparacoes_oficiais.csv`, `resumo.json`: the data, with no names or raw text.
- `fig_*.svg`: 5 charts.
- `build_finding.py`: the script that regenerates everything.

## Follow-ups worth a task

- Verify the 16 relatos still unverified, mostly new phone numbers, with an active round of calls.
- Normalize the ES comparison (SESA-ES) the same way as PR before quoting "100%" in a proposal.
- Ask SESA-PR to clarify scope: "locais de aplicação" (state) versus "pontos estratégicos" (MS).
