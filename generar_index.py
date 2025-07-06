import os

# Carpeta raíz para escanear: "." es la carpeta actual del repo
root_dir = "."

def generate_file_list(path):
    """
    Genera una lista recursiva de archivos y carpetas en estructura HTML.
    """
    items = []
    for entry in sorted(os.listdir(path)):
        if entry.startswith(".") or entry in ["index.html", os.path.basename(__file__)]:
            continue  # Ignora ocultos, index.html y este script
        full_path = os.path.join(path, entry)
        rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
        if os.path.isdir(full_path):
            subitems = generate_file_list(full_path)
            if subitems:
                items.append(f'<li>{entry}/<ul>{subitems}</ul></li>')
        else:
            items.append(f'<li><a href="{rel_path}" download>{rel_path}</a></li>')
    return "\n".join(items)

html_header = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Descargas automáticas</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    ul { list-style-type: none; }
    li { margin: 5px 0; }
  </style>
</head>
<body>
  <h1>Archivos disponibles para descarga</h1>
  <ul>
"""

html_footer = """
  </ul>
</body>
</html>
"""

print("Generando index.html...")
file_list_html = generate_file_list(root_dir)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_header + file_list_html + html_footer)

print("index.html generado con éxito.")
