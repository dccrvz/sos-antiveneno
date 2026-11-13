#!/usr/bin/env python3
"""Consolidate SoroJá public correction reports into a documented finding.

Inputs
- Control Sheet "Error Reports Summary V2" (private Google Sheet), read on
  2026-11-13. Its 364 rows were classified by hand below. Reporter names,
  e-mails and raw report text are deliberately NOT copied here (LGPD-minimal).
- app/hospitals.json (published dataset) as the denominator.
- data/location_overrides.json (two verified pin fixes that predate the Sheet).

Outputs (same folder): relatos_publico.csv, comparacoes_oficiais.csv,
resumo.json, fig_*.svg. Run from the repo root:
    python3 reports/public-corrections-2026-11/build_finding.py
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1. Public reports (one line per Sheet row that is a NEW report from the
#    public or a municipal health secretariat writing through the public form).
#    registro: relato = new report; corroboracao = repeat of an earlier report.
# tipo:
#   telefone | localizacao_mapa | fechada_desativada | atendimento_em_outra_unidade
#   sem_estoque | unidade_ausente | erro_identidade_fonte | sugestao_produto | bug_site
# desfecho:
#   confirmado_corrigido      verified by maintainer (map/phone/PDF) and fixed
#   confirmado_fonte_oficial  confirmed by a state/municipal health authority
#   publicado_como_relato     shown as an unverified "Relato da comunidade"
#   nao_confirmado            checked; claim not supported by evidence
#   nao_acionavel             outside SoroJá's scope (e.g. unit absent from PESA)
#   pendente                  still awaiting verification
#   produto                   UX/content suggestion (not a data error)
# ---------------------------------------------------------------------------
PUBLIC = [
    # row, cnes, uf, municipio, data, fonte, registro, tipo, desfecho
    ("pre", "9164", "SP", "São José dos Campos", "2026-04-20", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    ("pre", "2082187", "SP", "Ribeirão Preto", "2026-04-20", "publico", "relato", "atendimento_em_outra_unidade", "confirmado_corrigido"),
    (350, "", "PI", "Teresina", "2026-04-20", "publico", "relato", "unidade_ausente", "pendente"),
    (2, "2080346", "SP", "São Paulo", "2026-04-22", "publico", "relato", "telefone", "publicado_como_relato"),
    (3, "2080583", "SP", "São Paulo", "2026-04-22", "publico", "relato", "telefone", "publicado_como_relato"),
    (4, "3626245", "RS", "Canoas", "2026-04-23", "publico", "relato", "fechada_desativada", "confirmado_fonte_oficial"),
    (5, "2063018", "SP", "Orindiúva", "2026-04-23", "publico", "relato", "telefone", "publicado_como_relato"),
    (6, "2086271", "SP", "Itapecerica da Serra", "2026-04-24", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (7, "9491252", "SP", "São José dos Campos", "2026-04-25", "publico", "relato", "erro_identidade_fonte", "confirmado_corrigido"),
    (8, "2086255", "SP", "Tatuí", "2026-04-25", "publico", "relato", "atendimento_em_outra_unidade", "publicado_como_relato"),
    (9, "2801566", "BA", "Condeúba", "2026-04-25", "publico", "relato", "telefone", "publicado_como_relato"),
    (10, "2122634", "MG", "Recreio", "2026-04-25", "publico", "relato", "telefone", "publicado_como_relato"),
    (11, "2585367", "PR", "Marmeleiro", "2026-04-26", "publico", "relato", "fechada_desativada", "publicado_como_relato"),
    (12, "2738252", "PR", "Cascavel", "2026-04-27", "publico", "relato", "fechada_desativada", "publicado_como_relato"),
    (13, "2034441", "SP", "Rio Claro", "2026-04-27", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (14, "2403331", "ES", "Venda Nova do Imigrante", "2026-04-28", "publico", "relato", "sugestao_produto", "produto"),
    (15, "8000956", "MG", "Conselheiro Lafaiete", "2026-04-29", "publico", "relato", "atendimento_em_outra_unidade", "confirmado_fonte_oficial"),
    (16, "2569701", "GO", "São Domingos", "2026-04-29", "publico", "relato", "fechada_desativada", "nao_confirmado"),
    (17, "6483089", "MA", "Presidente Dutra", "2026-04-29", "publico", "relato", "telefone", "publicado_como_relato"),
    (18, "2738252", "PR", "Cascavel", "2026-05-01", "publico", "corroboracao", "fechada_desativada", "publicado_como_relato"),
    (19, "8000956", "MG", "Conselheiro Lafaiete", "2026-05-03", "publico", "corroboracao", "atendimento_em_outra_unidade", "confirmado_fonte_oficial"),
    (20, "2683202", "PR", "Ponta Grossa", "2026-05-03", "publico", "relato", "atendimento_em_outra_unidade", "publicado_como_relato"),
    (21, "", "", "Geral", "2026-05-05", "publico", "relato", "sugestao_produto", "produto"),
    (22, "7964145", "BA", "Teixeira de Freitas", "2026-05-05", "publico", "relato", "fechada_desativada", "confirmado_corrigido"),
    (23, "4047184", "SP", "Araraquara", "2026-05-06", "publico", "relato", "atendimento_em_outra_unidade", "publicado_como_relato"),
    (24, "2535556", "GO", "Jataí", "2026-05-09", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (25, "2219564", "MG", "Montes Claros", "2026-05-10", "publico", "relato", "telefone", "publicado_como_relato"),
    (26, "2708078", "RJ", "Volta Redonda", "2026-05-12", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (27, "2134071", "MG", "Conceição do Mato Dentro", "2026-05-13", "secretaria_municipal", "relato", "unidade_ausente", "confirmado_fonte_oficial"),
    (28, "", "PE", "(cobertura estadual)", "2026-05-13", "publico", "relato", "unidade_ausente", "nao_acionavel"),
    (29, "2775999", "MG", "Passos", "2026-05-13", "publico", "relato", "erro_identidade_fonte", "confirmado_corrigido"),
    (30, "2738252", "PR", "Cascavel", "2026-05-21", "publico", "corroboracao", "fechada_desativada", "publicado_como_relato"),
    (31, "7802951", "MG", "Carmo do Paranaíba", "2026-05-30", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (32, "2082519", "SP", "Paraguaçu Paulista", "2026-06-09", "publico", "relato", "telefone", "publicado_como_relato"),
    (33, "3626245", "RS", "Canoas", "2026-06-15", "publico", "corroboracao", "fechada_desativada", "confirmado_fonte_oficial"),
    (34, "7889046", "MT", "Bom Jesus do Araguaia", "2026-06-18", "publico", "relato", "telefone", "publicado_como_relato"),
    (35, "2342073", "GO", "Alto Paraíso de Goiás", "2026-07-15", "publico", "relato", "sem_estoque", "publicado_como_relato"),
    (36, "3626245", "RS", "Canoas", "2026-07-18", "publico", "corroboracao", "fechada_desativada", "confirmado_fonte_oficial"),
    (37, "2738252", "PR", "Cascavel", "2026-07-21", "publico", "corroboracao", "fechada_desativada", "publicado_como_relato"),
    (38, "3626245", "RS", "Canoas", "2026-07-23", "publico", "corroboracao", "fechada_desativada", "confirmado_fonte_oficial"),
    (39, "6053858", "SP", "Campinas", "2026-07-30", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (42, "2569701", "GO", "São Domingos", "2026-08-12", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (43, "2241021", "RS", "Bento Gonçalves", "2026-08-12", "publico", "relato", "unidade_ausente", "nao_confirmado"),
    (50, "4156714", "AL", "Maceió", "2026-08-17", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (341, "2692101", "MG", "Belo Horizonte", "2026-08-23", "publico", "relato", "telefone", "pendente"),
    (351, "3626245", "RS", "Canoas", "2026-10-03", "publico", "corroboracao", "fechada_desativada", "confirmado_fonte_oficial"),
    (352, "2687038", "PR", "Jaguariaíva", "2026-10-06", "publico", "relato", "telefone", "confirmado_fonte_oficial"),
    (355, "2285150", "RJ", "Araruama", "2026-10-13", "publico", "relato", "localizacao_mapa", "confirmado_corrigido"),
    (363, "8000956", "MG", "Conselheiro Lafaiete", "2026-10-14", "publico", "relato", "localizacao_mapa", "pendente"),
    (364, "2184680", "MG", "Rio Paranaíba", "2026-10-16", "publico", "relato", "atendimento_em_outra_unidade", "publicado_como_relato"),
    (365, "2417456", "BA", "Itarantim", "2026-10-22", "publico", "relato", "bug_site", "pendente"),
]
# Sheet rows NOT counted above because they are follow-ups/publication logs,
# not new reports: 40, 41, 44-49 (SESAU-AL), 51, 353, 354. Rows 52-340 and
# 342-349, 356-362 are official-source comparisons (section 2).

# ---------------------------------------------------------------------------
# 2. Official-source discrepancies (state health secretariat vs. federal MS
#    PESA list of 03/07/2026). Counts from the Sheet and from
#    reports/pr_sesa_ms_reconciliation_2026-10-09.md and
#    reports/pe_state_federal_reconciliation_2026-10-09.md.
# ---------------------------------------------------------------------------
OFFICIAL = [
    # uf, fonte_estadual, data, linhas_planilha, cnes_federais_no_estado,
    # federais_com_divergencia_ou_ausentes_no_estado, so_estadual, so_federal,
    # divergencias_de_campo (dict), situacao
    dict(uf="PR", fonte="SESA-PR (planilha 01/07/2026)", data="2026-08-25", linhas=207,
         federais=204, federais_divergentes=95 + 55, so_estadual=56, so_federal=55,
         campos={"antivenenos": 65, "telefone": 24, "nome": 14, "endereço": 8, "município": 1,
                 "colisão de CNES na planilha estadual": 5},
         situacao="1 telefone publicado (Jaguariaíva); restante aguarda esclarecimento da SESA-PR"),
    dict(uf="ES", fonte="SESA-ES (painel Vacina e Confia, 25/08/2026)", data="2026-08-25", linhas=65,
         federais=61, federais_divergentes=58 + 3, so_estadual=4, so_federal=3,
         campos={"endereço": 58, "telefone": 57, "nome/identidade": 46, "antivenenos": 21},
         situacao="aguardando confirmação de CNES/escopo com a SESA-ES"),
    dict(uf="PE", fonte="SES-PE (planilha 08/2026 + Ouve.PE 2026108606)", data="2026-08-20", linhas=24,
         federais=15, federais_divergentes=15, so_estadual=1, so_federal=0,
         campos={"telefone": 13, "endereço (material)": 2, "antivenenos": 2,
                 "classificação PEACA/identidade": 12, "unidade estadual distinta sob CNES compartilhado": 1},
         situacao="5 mudanças publicadas, 1 resolvida a favor do MS, 12 contatos pendentes"),
    dict(uf="RN", fonte="SESAP/RN (Ofício 2662/2026, 16/10/2026)", data="2026-10-16", linhas=7,
         federais=5, federais_divergentes=5, so_estadual=2, so_federal=1,
         campos={"antivenenos/classificação": 4, "unidade ausente na lista federal": 2,
                 "unidade federal omitida na lista estadual": 1},
         situacao="aguardando aprovação"),
    dict(uf="AL", fonte="SESAU-AL (resposta 13/08/2026)", data="2026-08-13", linhas=6,
         federais=16, federais_divergentes=2, so_estadual=1, so_federal=0,
         campos={"CNES errado (pertence a UBS)": 1, "unidade ausente na lista federal": 1,
                 "endereço/telefone desativado": 1},
         situacao="3 correções publicadas (PR #46) e pin corrigido (PR #48)"),
    dict(uf="MG", fonte="CNES/DATASUS + MS + SES-MG", data="2026-08-25", linhas=1,
         federais=295, federais_divergentes=3, so_estadual=0, so_federal=0,
         campos={"mesmo CNES atribuído a unidades em 4 municípios": 1},
         situacao="aguardando mapeamento correto da SES-MG"),
]

TIPO_PT = {
    "telefone": "Telefone errado ou sem resposta",
    "localizacao_mapa": "Localização/pin no mapa errado",
    "fechada_desativada": "Unidade fechada ou desativada",
    "atendimento_em_outra_unidade": "Atendimento feito em outra unidade",
    "sem_estoque": "Sem soro em estoque",
    "unidade_ausente": "Unidade ausente da lista",
    "erro_identidade_fonte": "Dados trocados/misturados na fonte",
    "sugestao_produto": "Sugestão de conteúdo/UX",
    "bug_site": "Bug do site (cartão duplicado)",
}
DESF_PT = {
    "confirmado_corrigido": "Confirmado e corrigido pelo SoroJá",
    "confirmado_fonte_oficial": "Confirmado por órgão de saúde",
    "publicado_como_relato": "Publicado como relato não verificado",
    "nao_confirmado": "Verificado e não confirmado",
    "nao_acionavel": "Fora do escopo (ausente da lista do MS)",
    "pendente": "Pendente",
    "produto": "Sugestão de produto",
}
DATA_ERROR_TYPES = set(TIPO_PT) - {"sugestao_produto", "bug_site"}
CONFIRMED = {"confirmado_corrigido", "confirmado_fonte_oficial"}


def svg_hbar(title, items, path, color="#2f6f5e", width=640):
    """Minimal horizontal bar chart as SVG (no external dependencies)."""
    bar_h, gap, left, top = 22, 8, 290, 44
    h = top + len(items) * (bar_h + gap) + 16
    mx = max(v for _, v in items) or 1
    plot_w = width - left - 50
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" '
        f'viewBox="0 0 {width} {h}" font-family="Helvetica, Arial, sans-serif">',
        f'<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="16" y="26" font-size="15" font-weight="bold" fill="#1d1d1d">{title}</text>',
    ]
    for i, (label, v) in enumerate(items):
        y = top + i * (bar_h + gap)
        w = max(1, plot_w * v / mx)
        parts.append(f'<text x="{left - 8}" y="{y + 15}" font-size="12" text-anchor="end" fill="#333">{label}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{left + w + 6:.1f}" y="{y + 15}" font-size="12" fill="#1d1d1d">{v}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_monthly(title, months, path, width=640):
    bar_w, gap, left, top, plot_h = 52, 18, 40, 44, 160
    h = top + plot_h + 50
    mx = max(v for _, v in months) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" '
        f'viewBox="0 0 {width} {h}" font-family="Helvetica, Arial, sans-serif">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="16" y="26" font-size="15" font-weight="bold" fill="#1d1d1d">{title}</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{width - 16}" y2="{top + plot_h}" stroke="#bbb"/>',
    ]
    for i, (m, v) in enumerate(months):
        x = left + 10 + i * (bar_w + gap)
        bh = plot_h * v / mx
        parts.append(f'<rect x="{x}" y="{top + plot_h - bh:.1f}" width="{bar_w}" height="{bh:.1f}" rx="3" fill="#2f6f5e"/>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{top + plot_h - bh - 6:.1f}" font-size="12" text-anchor="middle">{v}</text>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{top + plot_h + 18}" font-size="12" text-anchor="middle" fill="#333">{m}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main():
    hospitals = json.loads((ROOT / "app/hospitals.json").read_text(encoding="utf-8"))
    pub_cnes = {h["cnes"] for h in hospitals}
    per_uf = Counter(h["state"] for h in hospitals)
    total = len(hospitals)

    rows = [dict(zip(["linha_planilha", "cnes", "uf", "municipio", "data", "fonte", "registro", "tipo", "desfecho"], r))
            for r in PUBLIC]
    for r in rows:
        r["publicada_no_soroja"] = "sim" if r["cnes"] in pub_cnes else ("n/a" if not r["cnes"] else "não")
        r["tipo_pt"] = TIPO_PT[r["tipo"]]
        r["desfecho_pt"] = DESF_PT[r["desfecho"]]

    with (OUT / "relatos_publico.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    new = [r for r in rows if r["registro"] == "relato"]
    data_new = [r for r in new if r["tipo"] in DATA_ERROR_TYPES]
    # Unit-level view: one outcome per published CNES (best evidence wins).
    rank = ["confirmado_corrigido", "confirmado_fonte_oficial", "pendente", "publicado_como_relato",
            "nao_confirmado", "nao_acionavel"]
    unit_outcome = {}
    unit_types = defaultdict(set)
    for r in rows:
        if r["tipo"] not in DATA_ERROR_TYPES or r["publicada_no_soroja"] != "sim":
            continue
        unit_types[r["cnes"]].add(r["tipo"])
        cur = unit_outcome.get(r["cnes"])
        if cur is None or rank.index(r["desfecho"]) < rank.index(cur):
            unit_outcome[r["cnes"]] = r["desfecho"]
    units_reported = len(unit_outcome)
    units_confirmed = sum(1 for v in unit_outcome.values() if v in CONFIRMED)
    units_not_confirmed = sum(1 for v in unit_outcome.values() if v == "nao_confirmado")
    units_relato = sum(1 for v in unit_outcome.values() if v == "publicado_como_relato")
    units_pending = sum(1 for v in unit_outcome.values() if v == "pendente")

    # Official comparisons
    off_rows = []
    for o in OFFICIAL:
        off_rows.append({
            "uf": o["uf"], "fonte_estadual": o["fonte"], "data": o["data"], "linhas_planilha": o["linhas"],
            "unidades_federais_publicadas_no_estado": o["federais"],
            "federais_com_divergencia_ou_ausentes_na_lista_estadual": o["federais_divergentes"],
            "pct_federais_divergentes": round(100 * o["federais_divergentes"] / o["federais"], 1),
            "so_na_lista_estadual": o["so_estadual"], "so_na_lista_federal": o["so_federal"],
            "divergencias_por_campo": "; ".join(f"{k}: {v}" for k, v in o["campos"].items()),
            "situacao": o["situacao"],
        })
    with (OUT / "comparacoes_oficiais.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(off_rows[0].keys()))
        w.writeheader()
        w.writerows(off_rows)

    audited_ufs = ["PR", "ES", "PE", "RN"]
    audited_units = sum(o["federais"] for o in OFFICIAL if o["uf"] in audited_ufs)
    audited_div = sum(o["federais_divergentes"] for o in OFFICIAL if o["uf"] in audited_ufs)

    months = Counter(r["data"][:7] for r in rows if r["registro"] == "relato")
    all_months = [f"2026-{m:02d}" for m in range(4, 11)]
    month_items = [(m[5:] + "/" + m[2:4], months.get(m, 0)) for m in all_months]

    resumo = {
        "gerado_em": "2026-11-13",
        "fonte": "Control Sheet 'Error Reports Summary V2' (364 linhas, 22/04–22/10/2026) + 2 correções anteriores ao formulário em data/location_overrides.json",
        "periodo_relatos_publico": [min(r["data"] for r in rows), max(r["data"] for r in rows)],
        "unidades_publicadas_soroja": total,
        "linhas_planilha_total": 364,
        "linhas_relatos_publico_total": len(rows),
        "relatos_novos": len(new),
        "corroboracoes": len(rows) - len(new),
        "relatos_novos_sobre_dados": len(data_new),
        "relatos_por_tipo": Counter(r["tipo_pt"] for r in new),
        "relatos_por_desfecho": Counter(r["desfecho_pt"] for r in new),
        "relatos_por_uf": Counter(r["uf"] or "geral" for r in new),
        "relatos_por_mes": dict(sorted(months.items())),
        "unidades_publicadas_com_relato_de_erro": units_reported,
        "pct_unidades_publicadas_com_relato": round(100 * units_reported / total, 2),
        "unidades_com_erro_confirmado": units_confirmed,
        "unidades_relato_nao_verificado": units_relato,
        "unidades_pendentes": units_pending,
        "unidades_nao_confirmadas": units_not_confirmed,
        "relatos_verificados": sum(1 for r in data_new if r["desfecho"] in CONFIRMED | {"nao_confirmado"}),
        "relatos_verificados_confirmados": sum(1 for r in data_new if r["desfecho"] in CONFIRMED),
        "taxa_confirmacao_relatos_verificados": round(100 * sum(1 for r in data_new if r["desfecho"] in CONFIRMED)
            / max(1, sum(1 for r in data_new if r["desfecho"] in CONFIRMED | {"nao_confirmado"})), 1),
        "comparacoes_oficiais_linhas": sum(o["linhas"] for o in OFFICIAL),
        "ufs_auditadas_contra_lista_estadual": audited_ufs,
        "unidades_federais_nas_ufs_auditadas": audited_units,
        "unidades_federais_divergentes_nas_ufs_auditadas": audited_div,
        "pct_divergentes_ufs_auditadas": round(100 * audited_div / audited_units, 1),
    }
    (OUT / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    svg_hbar("Relatos novos do público, por tipo (n=%d)" % len(new),
             Counter(r["tipo_pt"] for r in new).most_common(), OUT / "fig_relatos_por_tipo.svg")
    svg_hbar("Relatos novos do público, por desfecho (n=%d)" % len(new),
             Counter(r["desfecho_pt"] for r in new).most_common(), OUT / "fig_relatos_por_desfecho.svg",
             color="#8a5a2b")
    svg_hbar("Relatos novos do público, por UF (n=%d)" % len(new),
             Counter(r["uf"] or "Geral" for r in new).most_common(), OUT / "fig_relatos_por_uf.svg",
             color="#3b5b8c")
    svg_monthly("Relatos novos do público por mês (2026)", month_items, OUT / "fig_relatos_por_mes.svg")
    svg_hbar("Unidades da lista federal (MS) que divergem da lista estadual (%)",
             [(f'{o["uf"]} ({o["federais_com_divergencia_ou_ausentes_na_lista_estadual"]}/'
               f'{o["unidades_federais_publicadas_no_estado"]})', o["pct_federais_divergentes"])
              for o in off_rows if o["uf"] in audited_ufs],
             OUT / "fig_divergencia_estado_vs_federal.svg", color="#a33b3b")

    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
