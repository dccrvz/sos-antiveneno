#!/usr/bin/env python3
"""Fetch the Receita Federal CNPJ record (via BrasilAPI) for every CNPJ found in cnes_raw.json
-> cnpj_raw.json (gitignored). Municipal units usually carry the Fundo Municipal de Saúde CNPJ,
so its phone is often the town health department, not the hospital itself."""
import json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
cnes = json.load(open(HERE / "cnes_raw.json"))
ids = sorted({v.get(k) for v in cnes.values() for k in ("numero_cnpj", "numero_cnpj_entidade")
              if isinstance(v, dict) and v.get(k)})
API = "https://brasilapi.com.br/api/cnpj/v1/{}"


def get(c):
    err = ""
    for a in range(4):
        try:
            req = urllib.request.Request(API.format(c), headers={"User-Agent": "soroja-number-hunt/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            keep = {k: d.get(k) for k in ("cnpj", "razao_social", "nome_fantasia", "ddd_telefone_1",
                                          "ddd_telefone_2", "municipio", "uf", "descricao_situacao_cadastral")}
            return c, keep
        except Exception as e:
            err = str(e); time.sleep(3 + a * 5)
    return c, {"error": err}


with ThreadPoolExecutor(3) as ex:
    res = dict(ex.map(get, ids))
json.dump(res, open(HERE / "cnpj_raw.json", "w"), ensure_ascii=False)
print(len(ids), "CNPJs;", sum("error" in v for v in res.values()), "errors")
