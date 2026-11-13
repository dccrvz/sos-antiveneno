# Validação de telefones: amostra de 50 unidades (13/11/2026)

**Resumo:** em 50 unidades sorteadas, **12% não têm um número utilizável** (sem telefone ou com número que não completa a ligação do jeito que está publicado). Outros **36% têm um número que nenhuma fonte independente confirma**. A taxa de falha real fica, portanto, entre **12% e 48%**. Só ligando para as unidades dá para estreitar essa faixa. Nenhuma unidade foi contatada (nem ligação, nem mensagem, nem e-mail).

## Método

- **População:** `app/hospitals.json` publicado, com 2.279 unidades em 25 UFs, todas com `source_date` 2026-07-03.
- **Sorteio:** amostra aleatória simples, sem reposição, de 50 unidades. As unidades foram ordenadas por (UF, CNES, nome) e sorteadas com `random.Random(20261113).sample(range(2279), 50)` em Python 3. **Seed: 20261113.** Para reproduzir: `python3 sample_and_check.py`.
- **Verificações, nesta ordem:**
  1. **Formato e DDD (offline).** Confere a quantidade de dígitos, se o número é fixo ou celular (celular precisa ter 9 dígitos e começar com 9), se o DDD é usado na UF e, numa conferência manual, se é o DDD do município.
  2. **CNES.** Puxei o registro de cada CNES na API de dados abertos do Ministério da Saúde (`apidadosabertos.saude.gov.br/cnes/estabelecimentos/{cnes}`; arquivo `fetch_cnes.py`) e comparei os últimos 8 dígitos do número publicado com os do CNES (arquivo `compare_cnes.py`). Também conferi se o município cadastrado no CNES bate com o da listagem.
  3. **Web.** Para os números que o CNES não confirma, fiz uma busca por unidade em páginas de prefeituras e secretarias, no site da própria unidade e em diretórios.
- **Classificação de cada número (arquivo `classify.py`):**
  - **válido:** formato e DDD corretos, e o número é confirmado pelo CNES ou por uma fonte independente. A lista PESA/MS **não conta** como confirmação, porque é a própria fonte do SoroJá.
  - **suspeito:** formato correto, mas o número não é confirmado: o CNES traz outro número ou nenhum, e a busca na web não achou nada. Também cai aqui o número com DDD incompatível com o município.
  - **inválido:** não completa a ligação do jeito que está publicado (formato impossível, ou DDD errado para a cidade quando o mesmo número aparece em outra fonte com o DDD certo).
  - **ausente:** a unidade não tem telefone publicado.
- **Status da unidade:** a unidade conta como OK se tiver pelo menos 1 número válido. Caso contrário, recebe o melhor status entre os seus números.
- **Intervalos de confiança:** IC de Wilson, 95%.

## Resultados

| Unidades (n=50) | n | % | IC 95% |
|---|---|---|---|
| Válida (≥1 número confirmado) | 26 | 52% | — |
| Só números suspeitos | 18 | 36% | — |
| Número inválido | 1 | 2% | — |
| Sem telefone | 5 | 10% | — |
| **Falha estrita** (ausente + inválido) | **6** | **12%** | **6%–24%** |
| **Falha ampla** (sem nenhum número confirmado) | **24** | **48%** | **35%–61%** |

- **Por número:** dos 49 números publicados, 26 são válidos, 22 suspeitos e 1 inválido. Ficam sem confirmação 47% (IC 34%–61%).
- **Formato:** nenhum número tem formato impossível. Todos os 49 têm a quantidade certa de dígitos, e todo DDD existe na UF. Os erros que aparecem são de **número trocado ou desatualizado**, não de digitação grosseira.

### Por UF

Com 1 a 8 unidades por UF, o detalhamento só serve como **indicação**. Não dá para tirar conclusão estatística por UF. Os números estão em `by_uf.csv`.

- **Sem nenhuma unidade confirmada:** MA (0 de 2) e PA (0 de 4). Nesses dois estados a lista do MS traz muitos celulares, e o CNES traz fixos, ou o contrário.
- **Melhores resultados:** GO (3 de 3) e PR (5 de 6).
- **Mais problemas:** BA (5 de 8 sem confirmação) e SP (4 de 7).

## Casos que merecem atenção

- **Hospital Rondon, Marechal Cândido Rondon (PR), inválido.** A listagem publica (44) 3284-7200, mas o DDD do município é 45, e outra fonte traz +55 45 3284-7200. Ligando com DDD 44, a chamada não chega ao hospital.
- **UPA Jequié (BA).** A listagem publica um celular com DDD 71 (Salvador), mas Jequié usa DDD 73. O CNES traz (73) 4103-0025.
- **UPA Campo Limpo (SP capital).** As três fontes divergem entre si. A listagem traz 5513-3132, o CNES traz 5511-6410 e a página da Secretaria Municipal de Saúde traz 5812-4688.
- **Santa Casa de Pereira Barreto (SP).** O número publicado e o do CNES diferem em 1 dígito (4255 × 4155). Pode ser erro de transcrição.
- **Unidades sem telefone (5):**
  - *Hospital São Francisco, Novo Repartimento (PA).* O CNES tem (94) 3785-1287, então dá para corrigir sem ligar.
  - *6º PEF, São Gabriel da Cachoeira (AM).* O registro CNES está **desativado** (motivo 08) e aponta para Pari-Cachoeira. A listagem pode estar apontando para o estabelecimento errado.
  - *Santa Casa de Itápolis (SP).* A linha publicada não tem CNES, endereço nem telefone.
  - *UPA de Itapetinga (BA) e PB Missão Marauia (AM).* Nenhum telefone foi achado, nem no CNES.
- **Problemas de cadastro no CNES** (não afetam a taxa de falha):
  - O CNES de Assis Chateaubriand (PR) traz o número certo, mas com DDD 45, que está errado.
  - O CNES 2086336 (Mairiporã, SP) tem nome fantasia "Hospital Infantil Menino Jesus". O telefone bate com a listagem.

## Limitações

- **O CNES também envelhece.** 37 dos 49 registros consultados foram atualizados pela última vez em 2025-09-03, data que parece ser de carga em lote. Um número "suspeito" não é necessariamente um número quebrado: pode ser que o CNES esteja desatualizado. Por isso a faixa de 12% a 48% é o resultado honesto.
- **A web ajuda pouco.** Hospitais municipais pequenos quase nunca publicam o telefone em página própria. A busca na web confirmou só 2 números a mais.
- **O teste não mede atendimento.** Confirma que o número existe e pertence à unidade, mas não que alguém atende 24h nem que a unidade tem soro em estoque.

## Próximo passo: ligar para as unidades (feito por uma pessoa)

`call_list.csv` lista as **24 unidades** sem número confirmado. Cada linha traz o(s) número(s) publicado(s), o número alternativo do CNES e colunas para anotar o resultado. Ligar primeiro para o número publicado e, se não completar, para o do CNES.

**Roteiro da ligação (cerca de 1 minuto):**

> Bom dia/boa tarde. Meu nome é ___, sou do projeto SoroJá, um guia público e gratuito de hospitais que aplicam soro antiveneno. Estamos conferindo os telefones da lista do Ministério da Saúde.
> 1. Aqui é o [nome da unidade], em [cidade]?
> 2. Este é o melhor número para o público ligar em caso de acidente com cobra, escorpião ou aranha? Se não for, qual é?
> 3. A unidade atende 24 horas?
> 4. (Opcional) A unidade continua sendo referência para soro antiveneno?
> Obrigado!

**Como registrar cada ligação:**

- Anotar `call_result` com um destes valores: `atendeu-correto`, `atendeu-outro-local`, `não completa`, `fora de área`, `ninguém atende (3 tentativas)` ou `número novo informado`.
- Não anotar o nome nem dados pessoais de quem atendeu (LGPD).
- Se uma ligação revelar um número melhor, corrigir pelo fluxo normal de override/nota comunitária, citando a fonte. Os dados publicados não foram alterados nesta etapa.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `phone_validation_sample50.csv` | 1 linha por número, com status e evidência |
| `call_list.csv` | 24 unidades para ligar, com colunas para anotar o resultado |
| `by_uf.csv` | Resultado por UF |
| `summary.txt` | Números consolidados |
| `offline_checks.csv`, `cnes_compare.csv`, `cnes_raw.json` | Dados intermediários |
| `sample_and_check.py`, `fetch_cnes.py`, `compare_cnes.py`, `classify.py` | Scripts para reproduzir, nesta ordem (`compare_cnes.py` recebe o JSON de municípios do IBGE, `servicodados.ibge.gov.br/api/v1/localidades/municipios?view=nivelado`) |
