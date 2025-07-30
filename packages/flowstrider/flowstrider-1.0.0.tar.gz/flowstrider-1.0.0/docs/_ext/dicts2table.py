# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import textwrap


def wrap_for_list_table(text, indent=5, width=72):
    lines = textwrap.wrap(str(text), width=width)
    if not lines:
        return [" " * indent + "-"]
    output = [f"{' ' * indent}- {lines[0]}"]
    output.extend([f"{' ' * (indent + 2)}{line}" for line in lines[1:]])
    return output


def generate_rst_table(data_dict):
    lines = []
    lines.append(".. list-table::")
    lines.append("   :widths: 20 30 20 30")
    lines.append("   :header-rows: 1\n")
    lines.append("   * - Field")
    lines.append("     - Description")
    lines.append("     - Applicable To")
    lines.append("     - Allowed Values")

    for field, values in data_dict.items():
        if len(values) != 4:
            raise ValueError(f"Expected 4 items for '{field}', got {len(values)}")

        label, desc, applicable, allowed = values
        desc = desc or ""
        applicable_str = ", ".join(str(x) for x in (applicable or []))
        allowed_str = ", ".join(str(x) for x in (allowed or []))
        lines.append(f"   * - ``{field}``")
        lines.extend(wrap_for_list_table(desc))
        lines.extend(wrap_for_list_table(applicable_str))
        lines.extend(wrap_for_list_table(allowed_str))
    return "\n".join(lines)


def setup(app):
    def write_table_file(app):
        import os

        from flowstrider.rules.attributes_dict import init_attributes

        init_attributes()
        from flowstrider.rules.attributes_dict import attributes

        out_dir = os.path.join(app.srcdir, "_generated")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "attributes_dict_table.rst")
        with open(path, "w") as f:
            f.write(generate_rst_table(attributes))

    app.connect("builder-inited", write_table_file)
    return {"version": "1.0"}
