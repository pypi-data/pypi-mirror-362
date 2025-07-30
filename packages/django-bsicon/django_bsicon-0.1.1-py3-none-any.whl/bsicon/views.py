from django.views.generic import TemplateView
from django.templatetags.static import static
import json
import os

class IconSelectorView(TemplateView):
    template_name = 'bsicon/icon_selector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cargar metadatos de iconos
        metadata_path = os.path.join(
            os.path.dirname(__file__),
            'static/bsicon/bootstrap-icons-metadata.json'
        )
        with open(metadata_path, 'r') as f:
            icons = json.load(f)
        
        context['icons'] = icons
        context['styles'] = sorted(set(
            style for icon in icons for style in icon['styles']
        ))
        return context
