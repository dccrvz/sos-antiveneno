# FAPESP PIPE Phase 1: SoroJá proposal outline

_Draft prepared 2026-11-15 (Claude Code) for Edu. Nothing has been submitted and nobody has been
contacted. Structure and notes are in English. The draft paragraphs are in pt-BR because they will be
pasted into SAGe as they are. Open decisions and missing inputs are in [`GAPS.md`](GAPS.md)._

## 0. Deadline and checklist

### What actually opens on 2026-11-16

FAPESP's PIPE Jornada page lists **"8ª Chamada – Geral – data de lançamento: 16/11/2026"**
([fapesp.br/pipejornada](https://fapesp.br/pipejornada), read 2026-11-15). On 2026-11-15 the text of
this call was **not yet published**, so its deadlines and limits below are **estimates from the
previous general call** (1ª Rodada 2026: launched 29/06, pre-proposal due 29/07, full proposal due
28/09; [fapesp.br/pipe/jornada-tecnologica-2026-fase-1](https://fapesp.br/pipe/jornada-tecnologica-2026-fase-1)).
Re-read the real call on 16/11 and fix every date here.

Regular **PIPE Phase 1 has no deadline**: it takes proposals all year by continuous flow
([fapesp.br/pipe](https://fapesp.br/pipe), [fapesp.br/pipe/normas](https://fapesp.br/pipe/normas) §9).
It is the fallback if the Jornada call is missed or turned down. The Jornada calls allow no
reconsideration, but a rejected proposal can be revised and sent to regular PIPE.

| Date                                              | What                                                                                   | Status                              |
| ------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------- |
| 2026-11-16                                        | 8th Jornada call ("Geral") published                                                   | Confirmed launch date; text pending |
| ~3 business days before the pre-proposal deadline | D.C. Cruz registered as a company in SAGe (FAPESP asks for at least 2–3 business days) | To do                               |
| **~2026-12-16 (estimate: launch + 30 days)**      | **Pre-proposal in SAGe**: 5 text fields, CVs (súmulas) and a 3-line budget             | Estimate                            |
| ~2027-02 (estimate: + 2 months)                   | Full proposal, only if the pre-proposal is accepted                                    | Estimate                            |
| ~2027-Q2 (estimate)                               | Results                                                                                | Estimate                            |
| Any time                                          | Regular PIPE Phase 1 (fallback)                                                        | Open now                            |

### Checklist

**Blocking (no submission without these, see GAPS.md):**

- [ ] Decide the route: Jornada 8th call (12 months, up to R$ 500k if it matches the 1ª Rodada) or regular Phase 1 (9 months, up to R$ 300k).
- [ ] D.C. Cruz meets the company rules: a for-profit company (not MEI or sole trader), ≤250 employees, head office or R&D unit in SP state with real physical space (no virtual address), and a corporate purpose that fits the project. It is registered in SAGe.
- [ ] Principal Investigator (PR): a partner with power to represent D.C. Cruz, living in SP state for the whole project. Check the Bolsa PE exclusivity rule against Edu's other work.
- [ ] Decide on a Principal Researcher (PP), if Edu is not the technical lead: needs ≥24 h/week and a formal tie to the company.
- [ ] Sign off the research question and the innovation angle (§2 below).
- [ ] Budget, split into capital, running costs and scholarships, with a justification for each item.
- [ ] IP position, given that the repo is public and open source (ADR 0002).
- [ ] Súmula curricular for the PR and each PP ([fapesp.br/sumula](https://fapesp.br/sumula)); Lattes and LinkedIn up to date; every team member registered in SAGe and confirmed on the proposal.

**Full-proposal stage (if the pre-proposal is accepted):**

- [ ] Project text on the official template, Anexo 1 ([pipeanexo1-2026.docx](https://fapesp.br/files/upload/58/pipeanexo1-2026.docx)): ≤25 pages, A4, Calibri/Arial 12, 1.5 spacing, margins 3 cm left and 1.5 cm right. No cover page; items may not be renumbered or removed. Title, abstract and bibliography don't count toward the 25 pages.
- [ ] Anexo II (company infrastructure statement) and the legal representative's statement (both templates in SAGe).
- [ ] Articles of association, proof of the company's address in its own name, and contracts with any outside team member or consultant.
- [ ] Commercial quotes for third-party services and consultants (the consultancy cap is R$ 50k in total).
- [ ] Nice to have: partner or support letters, usage metrics, LAI requests already filed.

## 1. Call rules (as read on 2026-11-15)

| Rule                    | Regular PIPE Phase 1                                | Jornada 1ª Rodada 2026 (model for the 8th call) |
| ----------------------- | --------------------------------------------------- | ----------------------------------------------- |
| Submission              | Continuous flow                                     | Pre-proposal, then a full proposal if accepted  |
| Duration                | Up to 9 months                                      | Up to 12 months                                 |
| Max funding             | R$ 300,000                                          | R$ 500,000                                      |
| Not counted in the cap  | Complementary benefits; direct infrastructure share | Same                                            |
| Phase 2                 | Phase 2 Indireta, from the month-6 progress report  | Phase 2 Indireta from month 8                   |
| Topics                  | Any                                                 | Any area (the 8th call is "Geral")              |
| One project per company | —                                                   | Yes, one per call                               |
| Reconsideration         | Yes                                                 | No (resubmit to regular PIPE)                   |

Sources: [Normas PIPE](https://fapesp.br/pipe/normas) (page updated 2026-09-28) §2.1, §5, §8–11;
[Jornada 1ª Rodada 2026](https://fapesp.br/pipe/jornada-tecnologica-2026-fase-1) §1–9;
[Anexo 1 template](https://fapesp.br/files/upload/58/pipeanexo1-2026.docx);
[scholarship values](https://fapesp.br/valores/bolsasnopais).

**Eligibility.**

- **PR:** a partner who is a natural person and can represent the company; lives in SP state.
- **PP:** proven capacity, ≥24 h/week, a formal tie to the company, lives in SP state; may not be an
  academic master's or PhD student.
- **Company:** ≤250 employees; head office or R&D unit in SP state (no virtual address); for-profit.
  MEI, sole traders, cooperatives, foundations and associations are not eligible. Inova Simples is
  allowed. For Phase 1 the company may be formed after the merit approval.
- **Team:** lives in SP state, mostly tied to the company, and combines scientific and business
  skills.

**What can be funded.**

- Consumables and equipment.
- Third-party services from legal entities (not core research).
- Consultancy, capped at R$ 50k in total.
- Travel and per diems.
- **Bolsa PE** (PE-I R$ 5,370, PE-II R$ 7,950, PE-III R$ 11,070 per month). It requires exclusive
  dedication of 40 h/week: no job, and the holder can't be managing partner of another company.
- **TT scholarships** (TT-III R$ 1,800, TT-IV R$ 4,520, TT-IV-A R$ 7,440, TT-V R$ 9,760 per month).
  A TT can't go to partners, employees, or relatives of partners.

**What FAPESP will not fund:**

- already-proven concepts;
- technical assistance;
- literature reviews;
- **market research**;
- confidential research;
- patent filing;
- "mere re-application of existing concepts".

**This is the main risk for SoroJá.** The proposal must be about a technical uncertainty, not about
running the app.

**Evaluation criteria (Normas §11.1.5, Jornada §8.5):**

| Criterion              | What reviewers check                                                                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (a) Research project   | Clear objectives; a plan and timeline; suitable method; challenge set against the state of the art; realistic timeframe; no third-party IP blocking the results |
| (b) Team               | PR/PP can lead; experience; complementary skills                                                                                                                |
| (c) Market             | Who suffers from the problem; why anyone would use or pay for the result; how the results will be exploited; efforts to raise other funding                     |
| (d) Scholarships       | Justified                                                                                                                                                       |
| (e) Budget             | Justified, sized right, for research and not production                                                                                                         |
| (f) Company conditions | Infrastructure, own staff, earlier grants                                                                                                                       |

**IP.** The company holds the IP. Third-party technology needs a licence. Service providers' IP
belongs to the company. In a collaboration IP may be shared, but the company must be able to exploit
the results exclusively.

## 2. Research question and innovation angle (proposal, needs Edu's sign-off)

Running the map is not research. The research is in the gap our own data has exposed. **Being on the
official list does not tell you whether a unit can give the right antivenom now.** No public source
answers that question.

**Proposed research question.** Can public, routinely published signals predict, with calibrated
probabilities, whether a listed Antivenom Strategic Point (PEA) is:

1. operating;
2. reachable by phone;
3. holding stock or depending on stock brought in from elsewhere (PEACA/PEASA).

The signals are: CNES status and unit type, SINAN antivenom notifications, state versus federal
lists, and structured citizen reports. Can these predictions, combined with road travel time, rank
units for someone who has just been bitten better than distance on the official list? And can they
point human verification at the units most likely to be wrong?

**Why this is uncertain (the technical risk):**

- There is no labelled ground truth. SIES (stock) and SI-PNI (doses given) are federal, mandatory for
  every PEA under NT 127/2026, and not published per unit.
- The signals are sparse, noisy and at municipality level. SINAN has no unit CNES.
- The base rates are unknown. In our sample of 50 units, 12% failed outright and 48% had no
  independent confirmation.
- Travel time to the nearest unit holding the _right_ antivenom has never been measured against the
  NT's ≤1h30 target.

**Innovation:** a per-unit operational reliability score, plus an accessibility model by antivenom
type, built from multiple sources and checked against field verification. Today's state of the art is
a static list from each state, as a PDF or a map.

**Phase 1 success metrics (draft):**

- **Labelled sample:** ≥300 units, stratified by UF and CNES type, using a documented verification
  protocol.
- **Calibration:** the model beats the "list as published" baseline (AUC, Brier score).
- **Verification targeting:** precision@k reduces the number of calls needed to find X% of faulty
  units by ≥Y% compared with random order. Edu sets X and Y.
- **Coverage map:** population beyond 1h30 by antivenom type and UF, with a sensitivity analysis.

## 3. Pre-proposal: SAGe "Campos adicionais" (Jornada format, with character limits)

Field names follow the 1ª Rodada 2026 call, §6.1(e). Check them against the 8th call. Drafts are in
pt-BR and within the limits as of this writing.

**1. O Problema e o "Pulo do Gato" (≤1.500 caracteres)**

> Quem é picado por serpente ou escorpião precisa chegar, em poucas horas, a uma unidade que tenha o
> soro certo e equipe para aplicá-lo; escorpionismo em crianças pode agravar em cerca de 2 h. O
> Ministério da Saúde publica os Pontos Estratégicos de Antivenenos (PEA) só como PDFs estaduais
> estáticos (2.279 unidades em jul/2026). Nossos dados mostram que estar na lista não garante
> atendimento: 107 códigos CNES publicados estão desativados ou não existem; em amostra aleatória,
> 12% das unidades não tinham telefone válido e 48% não tinham telefone confirmado de forma
> independente; em quatro estados, 81% das unidades federais divergem das listas estaduais. O SoroJá
> (soroja.com.br) já reúne a lista nacional em um app gratuito e offline. O "pulo do gato" é ir além
> da lista: estimar, por unidade, a probabilidade de ela estar operante, atender o telefone e ter
> estoque do soro certo agora, combinando sinais públicos (CNES, SINAN, listas estaduais, relatos
> verificados) com verificação de campo, e ordenar as opções pelo tempo real de deslocamento. Não
> encontramos solução pública ou comercial que faça isso no Brasil.

**2. A Incerteza Técnica (≤1.500 caracteres)**

> Não se sabe se sinais públicos, esparsos e agregados por município conseguem prever o estado
> operacional de cada unidade com precisão útil. Não há rótulo público: estoque (SIES) e doses
> aplicadas (SI-PNI) não são divulgados por unidade, e o SINAN não traz o CNES de quem aplicou o
> soro. Também não se sabe a distribuição real de falhas nem quanto a população está além da meta de
> 1h30 da NT 127/2026 por tipo de soro. Estágio atual: produto em produção com pipeline aberto de
> extração, geocodificação e auditoria das 27 UFs; camadas rastreáveis de correção; estudos
> preliminares cruzando a lista com CNES (2.227 unidades perfiladas) e com 37.703 casos de soroterapia
> do SINAN 2024 (91,3% em município com unidade listada; 154 municípios com 5 ou mais casos e
> nenhuma unidade listada; 206 municípios listados sem nenhum caso).

**3. Mãos à obra (≤2.000 caracteres)**

> E1 (meses 1–3): protocolo de verificação por telefone, padronizado e reprodutível (roteiro,
> critérios de "operante", "atende", "tem estoque"), e amostra estratificada por UF e tipo CNES;
> pedidos via LAI ao MS (SIES e SI-PNI por unidade) e às SES. E2 (meses 2–7): coleta de rótulos em
> pelo menos 300 unidades; engenharia de atributos a partir de CNES, SINAN 2024–2026, listas
> estaduais e relatos públicos. E3 (meses 5–9): modelos de escore de confiabilidade calibrado,
> comparados à linha de base "lista publicada"; métricas AUC, Brier e precisão@k para direcionar a
> verificação. E4 (meses 6–10): modelo de acessibilidade por rede viária e tipo de soro; mapa da
> população além de 1h30, com análise de sensibilidade. E5 (meses 9–12): validação prospectiva em
> nova amostra; protótipo de interface que mostra a confiabilidade ao usuário sem prometer estoque, e
> relatório técnico. Critério de sucesso: escore supera a linha de base e reduz em pelo menos [Y]% as
> ligações necessárias para achar [X]% das unidades com falha.

**4. Oportunidade de Mercado (≤1.500 caracteres)**

> Entregável: um serviço de dados de PEAs verificados, com escore de confiabilidade, acessibilidade
> por tipo de soro e API, além do app público, que segue gratuito. Quem paga: [DECISÃO DO EDU, ver
> GAPS] centrais de regulação SAMU 192, CIATox e secretarias de saúde, que precisam manter e divulgar
> a lista (NT 127/2026, §3.2.6 e §6.2), por contrato de dados e verificação; empresas com equipes em
> campo (agro, florestal, energia, mineração) e seguradoras ou telemedicina, por assinatura da API.
> O Brasil notifica dezenas de milhares de acidentes com animais peçonhentos por ano; só em 2024
> foram 37.703 casos com soroterapia.

**5. Quem vai fazer acontecer? (≤1.500 caracteres)**

> [PREENCHER COM A EQUIPE REAL, ver GAPS] PR: Eduardo [sobrenome], sócio da D.C. Cruz, criador e
> mantenedor do SoroJá desde abril de 2026: pipeline de dados, geocodificação, auditoria e app em
> produção. PP: [cientista de dados ou epidemiologista, ≥24 h/semana]. Consultoria: [toxicologista
> ou CIATox, até R$ 50 mil]. Bolsistas TT: verificação por telefone e curadoria. A D.C. Cruz
> [descrever: atividade, sede ou unidade em SP, infraestrutura].

**Budget (SAGe "R$/US$" tab, three headings):** capital, running costs and scholarships. See §4.10.

## 4. Full proposal: Anexo 1 sections (outline and draft paragraph for each)

Page guidance comes from the template. The total body must not exceed 25 pages.

### 4.1 Título

**Outline:** short, self-explanatory, no acronyms.

> **Draft:** _Confiabilidade operacional e acessibilidade dos Pontos Estratégicos de Antivenenos no
> Brasil: um modelo multifonte verificado em campo._

### 4.2 Resumo (~1 page; write it last)

**Outline:** cover problem → gap → objective → method → expected result → impact on the company and
the market.

> **Draft:** Acidentes por animais peçonhentos exigem soro específico em poucas horas, mas a lista
> oficial de Pontos Estratégicos de Antivenenos (PEA) é estática e, como mostram nossos levantamentos,
> contém unidades desativadas, telefones inválidos e divergências com as listas estaduais. Este
> projeto investiga se sinais públicos (CNES, SINAN, listas estaduais, relatos verificados),
> calibrados por uma amostra de verificação em campo, permitem estimar a confiabilidade operacional
> de cada PEA e ordenar as opções de atendimento pelo tempo real de deslocamento até o soro correto.
> Os resultados esperados são um escore validado, um mapa de acessibilidade por tipo de soro frente à
> meta de 1h30 da NT 127/2026 e um protótipo integrado ao SoroJá, a base de um serviço de dados para a
> rede de urgência.

### 4.3 Objetivos (≤2 pages)

**Outline:**

- **General objective:** (1) the score; (2) the accessibility model.
- **Specific objectives:** protocol; ≥300 labels; model versus baseline; accessibility map;
  prototype; prospective validation.
- **Innovation objective:** for D.C. Cruz, a data product; for the market, the first verified,
  per-unit reliability layer.

> **Draft:** Objetivo geral: desenvolver e validar um método que estime, para cada PEA, a
> probabilidade de estar operante, contatável e com estoque do soro adequado, e que integre essa
> estimativa ao cálculo de acessibilidade por tipo de soro. Objetivos específicos: (i) definir um
> protocolo de verificação reprodutível; (ii) rotular uma amostra estratificada de pelo menos 300
> unidades; (iii) treinar e calibrar modelos e compará-los com a linha de base "lista publicada";
> (iv) estimar a população além de 1h30 do soro adequado, por UF; (v) validar prospectivamente;
> (vi) prototipar a comunicação do grau de confiança ao usuário sem prometer estoque.

### 4.4 Informações sobre a empresa (≤2 pages)

**Outline:**

- (a) Corporate and administrative data.
- (b) R&D and IP holdings. Today: an open-source repo, a pipeline and a public dataset.
- (c) Counterpart and other funding.
- (d) Infrastructure, with photos.

**All D.C. Cruz data are missing** (GAPS §A).

> **Draft:** A D.C. Cruz [razão social, CNPJ, endereço em SP, número de empregados] atua em
> [atividade]. Desde 2026-11-14 é titular do repositório do SoroJá (github.com/dccrvz/sos-antiveneno),
> aplicativo web progressivo, gratuito e de código aberto, em produção em soroja.com.br. Ele cobre as
> 27 UFs, com pipeline automatizado de extração dos PDFs do Ministério, geocodificação, classificação
> de qualidade em várias camadas, camadas rastreáveis de correção oficial e comunitária, e
> verificação diária de atualizações. Contrapartida: [horas do PR e da equipe, hospedagem, ferramentas;
> doações via Pix].

### 4.5 Descrição da equipe (with the mandatory responsibilities table)

**Outline:** PR/PP qualifications; a table with name, responsibility, activity and period for every
member and scholarship holder.

> **Draft:** [GAPS §B]. The table must list the PR, the PP, the consultant(s) and each TT scholarship
> holder (named or "a definir"), with activities E1–E5 from §4.7.

### 4.6 Revisão da evolução científico-tecnológica (~3 pages)

**Outline:**

1. **Epidemiology:** antivenom treatment as time-critical care; scorpion stings in children; WHO
   priority (snakebite as a neglected tropical disease).
2. **The Brazilian model:**
   - The Ministry buys the full output of four producers (Butantan, Vital Brazil, Funed, CPPI) and
     distributes it monthly.
   - Stock moves through SIES and the cold chain.
   - NT 127/2026 sets the requirements for a PEA.
3. **Access and travel-time literature:** geographic accessibility to antivenom; two-step floating
   catchment and road-network methods.
4. **Data quality in health-facility registries:** CNES, and the gap between a facility's
   designation and the service it actually provides.
5. **Existing tools:**
   - MS PESA PDFs.
   - State maps and dashboards (SP CVE; GO SERKET).
   - CIATox phone lines.
6. **Patents and FTO:** INPI and Google Patents search (to do).
7. **Research groups:** Butantan, CIATox network, Fiocruz, universities.

**Needs a real literature search with citations.** None are invented here.

> **Draft:** A literatura sobre acesso a antivenenos mede distância a serviços designados, mas
> assume que designação equivale a capacidade de atendimento. Levantamentos institucionais recentes
> (incluindo os nossos) mostram que designação, capacidade de aplicar, armazenamento local,
> abastecimento regular e estoque corrente são fatos distintos, e que nenhuma fonte pública os
> informa por unidade. [Completar com referências revisadas.]

### 4.7 Plano de pesquisa (~10 pages)

**Outline:**

- (b) Methods:
  - verification protocol and sampling;
  - data sources;
  - features;
  - models (calibrated classifiers; hierarchical by UF);
  - accessibility (road-network routing per antivenom type);
  - evaluation (AUC, Brier, precision@k, calibration plots);
  - LGPD design: no patient data, no reporter PII, and geolocation stays on the device.
- (c) Activities E1–E5, each tied to an uncertainty, with the owner named.
- (d) Timeline with milestones.
- (e) Deliverables.
- Item (a), earlier results, is only for Phase 2. Keep the preliminary findings in 4.6 or 4.4.

| Stage                                      | Months (12-month Jornada) | Uncertainty addressed                                                                          | Deliverable                                |
| ------------------------------------------ | ------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------ |
| E1 Protocol and sampling; LAI requests     | 1–3                       | Can "operating / reachable / has stock" be measured reliably by phone? (inter-rater agreement) | Protocol v1, sampling frame, LAI log       |
| E2 Labelling and features                  | 2–7                       | Base rates of failure by UF and type                                                           | ≥300 labelled units; feature dataset       |
| E3 Reliability model                       | 5–9                       | Do public signals predict status better than the list?                                         | Model and evaluation report                |
| E4 Accessibility by antivenom type         | 6–10                      | Population beyond 1h30, by type                                                                | Coverage map and sensitivity analysis      |
| E5 Prospective validation and UX prototype | 9–12                      | Does the score hold on fresh data? How should uncertainty be shown safely?                     | Validation report; prototype; Phase 2 plan |

For the regular 9-month route, compress E4 and E5 or move E5 to Phase 2.

### 4.8 Competidores, PI e liberdade de operação (~2 pages)

**Outline:**

- **Competitors and substitutes:**
  - MS PESA PDFs;
  - state lists and maps;
  - CIATox and Disque-Intoxicação;
  - SAMU regulation (internal lists);
  - generic maps (Google Maps: no antivenom data);
  - international antivenom-locator apps (search needed).
- **Advantages:** national coverage; type-specific; offline; auditable layers; and, new, the
  reliability score and verified data.
- **IP:** open-source code (ADR 0002) versus what D.C. Cruz will own. See GAPS §F.
- **FTO search:** INPI and Google Patents.

> **Draft:** Não identificamos solução que combine cobertura nacional, filtragem por tipo de soro e
> uma medida de confiabilidade por unidade. As listas estaduais e o próprio Ministério publicam
> designações, não estado operacional. [Completar após busca de patentes e concorrentes.]

### 4.9 Potencial comercial (≤2 pages, with a 5-year estimate)

**Outline:** beneficiaries; customers and payers; business model (bullet points); a 5-year table
of customers and revenue or avoided cost; quantitative where possible.

**Edu must choose the model** (GAPS §E). Keep the public app free.

> **Draft:** Beneficiários diretos: vítimas e familiares, sobretudo em áreas rurais. Clientes
> potenciais: (1) gestores públicos responsáveis pela lista de PEA e por sua divulgação a SAMU e
> CIATox; (2) empresas com trabalhadores expostos (agro, florestal, energia, mineração), cuja gestão
> de risco ocupacional precisa de um plano de resposta a acidentes; (3) operadoras e serviços de
> telemedicina. Modelo: app público gratuito e de código aberto; receita com licença ou assinatura de
> dados verificados e API, e com contratos de verificação e manutenção da lista. [Tabela de 5 anos:
> preencher.]

### 4.10 Orçamento detalhado e justificado (≤2 pages)

**Illustrative only (not a recommendation): a 12-month Jornada route, using scholarship values from
01/08/2025.** Edu decides every line (GAPS §D).

| Item                                                | Heading       | Basis                          | Estimate (R$) |
| --------------------------------------------------- | ------------- | ------------------------------ | ------------: |
| Bolsa PE (PP, data science/epidemiology)            | Scholarships  | PE-II 7,950 × 12               |        95,400 |
| 2 × Bolsa TT (verification and curation)            | Scholarships  | TT-IV 4,520 × 12 × 2           |       108,480 |
| Consultancy (clinical toxicology / epidemiology)    | Running costs | cap R$ 50k                     |        40,000 |
| Road-network routing and geocoding APIs; cloud      | Running costs | quotes needed                  |        30,000 |
| Telephony for verification calls                    | Running costs | quotes needed                  |         6,000 |
| Travel and per diems (CIATox/SAMU field visits, SP) | Running costs | estimate                       |        15,000 |
| Equipment (workstation)                             | Capital       | 3 quotes if > 10 minimum wages |        12,000 |
| **Total requested**                                 |               |                                |  **≈306,880** |

This total is below the Jornada cap (R$ 500k) but above the regular 9-month cap (R$ 300k). On the
regular route, cut the months.

### 4.11 Cronograma físico-financeiro

**Outline:** the template table (activity, owner, budget item, cost, months 1–12), one row per E1–E5
activity. Fill it in after the budget is final.

### 4.12 Bibliografia

**Outline:** ABNT NBR 6023 or APA; a separate subsection for patents. Starting sources already in the
repo:

- NT Conjunta 127/2026-SVSA/SAPS/SAES/SESAI/MS
  ([gov.br](https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/notas-tecnicas/2026/nota-tecnica-conjunta-no-127-2026-svsa-saps-saes-sesai-ms.pdf));
- SINAN microdata (DATASUS FTP);
- the CNES open-data API;
- the MS PESA per-UF pages;
- the MS CIATox directory.

## 5. Evidence map (where each number comes from)

| Claim                                                                      | Source in this repo                                                                             |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 2,279 units, 27 UFs, PESA 2026-07-03                                       | `app/hospitals.json`, `docs/CONTEXT.md`                                                         |
| 107 CNES inactive or missing; 2,227 profiled; ~260 not 24h                 | `reports/hospital-value-2026-11/FINDINGS.md` (**uncommitted, main checkout only**, see GAPS §G) |
| SINAN 2024: 37,703 antivenom cases; 91.3%; 154 / 50 / 206 municipalities   | same                                                                                            |
| NT 127/2026: PEACA/PEASA, ≤1h30, SIES/SI-PNI mandatory, ~2,319 units       | same, which cites the NT PDF                                                                    |
| 12% strict failure, 48% unconfirmed phone (n=50)                           | `reports/phone-validation-2026-11/`                                                             |
| 18/20 reports confirmed; 231/285 (81%) state-federal divergence            | `reports/public-corrections-2026-11/`                                                           |
| State contact routes; ordering through SIES and the immunisation programme | `Soroja_deepresearch/` (main checkout, untracked)                                               |

### Conflict to resolve before submission

The two deep-research files disagree about NT 127/2026:

- The Gemini report and FINDINGS.md (which read the NT PDF) say it defines **PEACA/PEASA**.
- The Claude "compass" report (July 2026) says the MS document it found doesn't use those acronyms.
  It reported a "Pontos Estratégicos de Antivenenos (PEA)" note dated 25/05/2026 that separates
  receiving, storage and administration.

Re-read the NT PDF and quote the exact section before reviewers see it.
