# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import re
from typing import List, Tuple


def extract_attributes_from_docstring(docstring: str) -> List[Tuple[str, str, str]]:
    if not docstring:
        return []
    lines = docstring.expandtabs().splitlines()
    attributes = []
    in_attr_section = False
    current_attr = None
    current_desc = []

    for line in lines:
        stripped = line.strip()
        if not in_attr_section and stripped.lower() == "attributes:":
            in_attr_section = True
            continue
        if in_attr_section and re.match(r"^[A-Z][A-Za-z0-9_ ]+:$", stripped):
            break
        if in_attr_section:
            match = re.match(r"^\s*(\w+)\s*\(([^)]+)\):\s*(.*)", line)
            if match:
                if current_attr:
                    attributes.append(
                        (
                            current_attr[0],
                            current_attr[1],
                            " ".join(current_desc).strip(),
                        )
                    )
                    current_desc = []
                name, type_, desc = match.groups()
                current_attr = (name.strip(), type_.strip())
                if desc:
                    current_desc.append(desc.strip())
            elif current_attr:
                if stripped:
                    current_desc.append(stripped)
    if current_attr:
        attributes.append(
            (current_attr[0], current_attr[1], " ".join(current_desc).strip())
        )

    return attributes


def format_rst_table(attributes):
    lines = [
        ".. list-table::",
        "   :widths: 20 30 20",
        "   :header-rows: 1\n",
        "   * - Field",
        "     - Description",
        "     - Type",
    ]

    for name, type_, desc in attributes:
        lines.append(f"   * - ``{name}``")
        lines.append(f"     - {desc}")
        lines.append(f"     - ``{type_}``")

    return "\n".join(lines)


def setup(app):
    def write_table_file(app):
        import os

        from flowstrider.models.common_models import Cluster, Edge, Node
        from flowstrider.models.dataflowdiagram import DataflowDiagram

        out_dir = os.path.join(app.srcdir, "_generated")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "dfd_class_table.rst"), "w") as f:
            f.write(
                format_rst_table(
                    extract_attributes_from_docstring(DataflowDiagram.__doc__ or "")
                )
            )
        with open(os.path.join(out_dir, "cluster_class_table.rst"), "w") as f:
            f.write(
                format_rst_table(
                    extract_attributes_from_docstring(Cluster.__doc__ or "")
                )
            )
        with open(os.path.join(out_dir, "edge_class_table.rst"), "w") as f:
            f.write(
                format_rst_table(extract_attributes_from_docstring(Edge.__doc__ or ""))
            )
        with open(os.path.join(out_dir, "node_class_table.rst"), "w") as f:
            f.write(
                format_rst_table(extract_attributes_from_docstring(Node.__doc__ or ""))
            )

    app.connect("builder-inited", write_table_file)
    return {"version": "1.0"}
