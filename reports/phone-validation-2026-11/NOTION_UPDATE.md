# Atualização para a tarefa do Notion

Tarefa: "SoroJá: rodar amostra de validação de telefones (50 unidades) e apurar % de falha"

O conector do Notion deu erro nas 4 tentativas de 13/11/2026. Copie o texto abaixo para a tarefa.

**Status:** Done (validação sem ligar). Se for fazer a rodada de ligações, abra uma tarefa nova.

**% de falha (texto para colar):**
Amostra aleatória de 50 unidades (seed 20261113) de 2.279. A falha estrita é de 12% (6 de 50; IC95% 6–24%): sem telefone ou com número que não completa a ligação. A falha ampla, contando as unidades sem nenhum número confirmado por CNES ou web, é de 48% (24 de 50; IC95% 35–61%). A taxa real está entre esses dois valores, e só ligações vão estreitar a faixa. Nenhum número tem formato impossível: os problemas são de número trocado ou desatualizado. MA (0 de 2) e PA (0 de 4) não tiveram nenhuma unidade confirmada.

**Para a proposta de patrocínio e o orçamento PIPE:** cerca de metade das unidades precisaria de ligação para ser confirmada. Isso dá cerca de 1.100 unidades no conjunto completo, se a proporção da amostra se mantiver.

**Arquivos:** `reports/phone-validation-2026-11/` no repositório (ainda não commitado):
- `ACHADOS.md`: relatório
- `phone_validation_sample50.csv`: 1 linha por número
- `call_list.csv`: 24 unidades para ligar, com roteiro no ACHADOS.md

**Próximo passo:** uma pessoa liga para as 24 unidades da `call_list.csv` usando o roteiro. Correção imediata possível: o Hospital São Francisco de Novo Repartimento (PA) não tem telefone publicado, mas o CNES tem (94) 3785-1287.
