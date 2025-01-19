from __future__ import annotations

import csv
import os
import re
import shutil
from pathlib import Path

HOME = "compiler/errors"
DEST = "pyrogram/errors/exceptions"


def snake(s):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def camel(s):
    s = snake(s).split("_")
    return "".join([str(i.title()) for i in s])


def start() -> None:
    shutil.rmtree(DEST, ignore_errors=True)
    Path(DEST).mkdir(parents=True, exist_ok=True)
    files = list(os.listdir(f"{HOME}/source"))

    with Path(DEST, "all.py").open("w", encoding="utf-8") as f_all:
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()
            f_all.write(f"    {code}: {{\n")
            init = f"{DEST}/__init__.py"

            with Path(init).open("a", encoding="utf-8") as f_init:
                f_init.write(f"from .{name.lower()}_{code} import *\n")

            with (
                Path(HOME, "source", i).open(encoding="utf-8") as f_csv,
                Path(DEST, f"{name.lower()}_{code}.py").open(
                    "w",
                    encoding="utf-8",
                ) as f_class,
            ):
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = camel(name)
                name = " ".join(
                    [
                        str(i.capitalize())
                        for i in re.sub(r"_", " ", name).lower().split(" ")
                    ],
                )

                sub_classes = []

                f_all.write(f'        "_": "{super_class}",\n')

                for j, row in enumerate(reader):
                    if j == 0:
                        continue

                    count += 1

                    if not row:  # Row is empty (blank line)
                        continue

                    error_id, error_message = row

                    sub_class = camel(re.sub(r"_X", "_", error_id))
                    sub_class = re.sub(r"^2", "Two", sub_class)
                    sub_class = re.sub(r" ", "", sub_class)

                    f_all.write(f'        "{error_id}": "{sub_class}",\n')

                    sub_classes.append((sub_class, error_id, error_message))

                with Path(HOME, "template/class.txt").open(
                    encoding="utf-8",
                ) as f_class_template:
                    class_template = f_class_template.read()

                    with Path(HOME, "template/sub_class.txt").open(
                        encoding="utf-8",
                    ) as f_sub_class_template:
                        sub_class_template = f_sub_class_template.read()

                    class_template = class_template.format(
                        super_class=super_class,
                        code=code,
                        docstring=f'"""{name}"""',
                        sub_classes="".join(
                            [
                                sub_class_template.format(
                                    sub_class=k[0],
                                    super_class=super_class,
                                    id=f'"{k[1]}"',
                                    docstring=f'"""{k[2]}"""',
                                )
                                for k in sub_classes
                            ],
                        ),
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with Path(DEST, "all.py").open(encoding="utf-8") as f:
        content = f.read()

    with Path(DEST, "all.py").open("w", encoding="utf-8") as f:
        f.write(re.sub("{count}", str(count), content))


if __name__ == "__main__":
    HOME = "."
    DEST = "../../pyrogram/errors/exceptions"

    start()
