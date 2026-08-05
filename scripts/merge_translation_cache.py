#!/usr/bin/env python3
"""Resolve o conflito do cache de traducao unindo os dois lados.

Quando duas execucoes do Action traduzem em paralelo, as duas reescrevem
scripts/translation-cache.json e o rebase para em conflito. Descartar um dos
lados joga fora traducao ja paga em cota, entao aqui os dois sao unidos: cada
lado so tem trechos que passaram pela API.

Le as versoes do indice do git durante o conflito -- :2 (nossa) e :3 (a que
chegou primeiro ao remoto) -- e grava o resultado por cima do arquivo.
"""
import json
import subprocess
import sys

CAMINHO = "scripts/translation-cache.json"


def do_indice(estagio):
    """Le uma das versoes em conflito. Estagio 2 = nossa, 3 = deles."""
    try:
        bruto = subprocess.run(
            ["git", "show", ":{}:{}".format(estagio, CAMINHO)],
            capture_output=True, check=True).stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        return None
    try:
        return json.loads(bruto)
    except ValueError:
        return None


def main():
    nosso = do_indice(2)
    deles = do_indice(3)
    if nosso is None and deles is None:
        print("nenhum dos lados e JSON valido; nada a unir")
        return 1

    lados = [d for d in (deles, nosso) if d]
    # Idiomas alvo diferentes nao se misturam: a traducao guardada e para outro
    # destino. Nesse caso vale a nossa, que acabou de ser gerada.
    alvos = {d.get("target_lang") for d in lados}
    if len(alvos) > 1:
        vencedor = nosso or deles
        print("alvos diferentes {}; ficando so com o nosso".format(sorted(alvos)))
        unido = vencedor
    else:
        entries = {}
        for d in lados:                     # o nosso vem por ultimo e prevalece
            entries.update(d.get("entries", {}))
        unido = {"target_lang": lados[0].get("target_lang"),
                 "entries": {k: entries[k] for k in sorted(entries)}}
        print("unidos: {} + {} -> {} trechos".format(
            len(deles.get("entries", {})) if deles else 0,
            len(nosso.get("entries", {})) if nosso else 0,
            len(unido["entries"])))

    with open(CAMINHO, "w", encoding="utf-8") as f:
        json.dump(unido, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
