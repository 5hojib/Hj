# ruff: noqa: E741
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import requests

if len(sys.argv) != 2:
    sys.exit(1)

if sys.argv[1] == "sort":
    for p in Path("source").glob("*.tsv"):
        with p.open() as f:
            reader = csv.reader(f, delimiter="\t")
            dct = {k: v for k, v in reader if k != "id"}
            keys = sorted(dct)

        with p.open("w") as f:
            f.write("id\tmessage\n")
            for i, item in enumerate(keys, start=1):
                f.write(f"{item}\t{dct[item]}")
                if i != len(keys):
                    f.write("\n")

elif sys.argv[1] == "scrape":
    b = "https://core.telegram.org"
    c = "/api/errors"
    a = requests.get(b + c)
    d = a.text
    e = r"\<a\ href\=\"(.*)\"\>here.*\<\/a\>"
    f = re.search(e, d)
    if f:
        a = requests.get(b + f.group(1))
        d = a.json()
        e = d.get("errors", [])
        for h in e:
            dct = {}
            j = d.get("errors").get(h)
            for k in j:
                if k.endswith("_*"):
                    continue
                g = d.get("descriptions")
                l = g.get(k)
                m = k.replace("_%d", "_X")
                l = l.replace("%d", "{value}")
                l = l.replace("&raquo;", "»")
                l = l.replace("&laquo;", "«")
                l = l.replace("](/api/", f"]({b}/api/")
                dct[m] = l

            for p in Path("source/").glob(f"{h}*.tsv"):
                with p.open() as f:
                    reader = csv.reader(f, delimiter="\t")
                    for k, v in reader:
                        if k != "id":
                            dct[k] = v

            keys = sorted(dct)

            for p in Path("source/").glob(f"{h}*.tsv"):
                with p.open("w") as f:
                    f.write("id\tmessage\n")
                    for _i, item in enumerate(keys, start=1):
                        f.write(f"{item}\t{dct[item]}\n")
