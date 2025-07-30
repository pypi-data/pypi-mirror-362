import requests
import json
import os

# Descargar iconos del repositorio oficial
response = requests.get('https://api.github.com/repos/twbs/icons/contents/icons?ref=main')
icons_data = response.json()

# Procesar metadatos
icons_metadata = []
for icon in icons_data:
    if icon['name'].endswith('.svg'):
        name = icon['name'][:-4]
        icons_metadata.append({
            'name': name,
            'search_terms': name.replace('-', ' '),
            'styles': ['outline']  # Bootstrap solo tiene un estilo
        })

# Guardar en archivo JSON
metadata_path = os.path.join(
    os.path.dirname(__file__),
    '../bsicon/static/bsicon/bootstrap-icons-metadata.json'
)

with open(metadata_path, 'w') as f:
    json.dump(icons_metadata, f)

print(f"Actualizados {len(icons_metadata)} iconos")
