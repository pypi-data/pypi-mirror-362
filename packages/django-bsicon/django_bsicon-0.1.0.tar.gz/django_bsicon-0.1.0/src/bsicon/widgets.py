from django.forms import TextInput
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

class BsIconWidget(TextInput):
    template_name = 'bsicon/icon_selector.html'

    class Media:
        css = {
            'all': ('bsicon/css/bootstrap-icons.min.css', 'bsicon/css/bsicon.css')
        }
        js = ('bsicon/js/list.min.js', 'bsicon/js/bsicon.js')

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        selector_url = reverse_lazy('bsicon_selector')
        html = f'''
        <div class="bsicon-wrapper">
            {output}
            <a href="{selector_url}" class="bsicon-selector-button" data-field-id="{attrs['id']}">
                <span class="current-icon">
                    {f'<i class="bi bi-{value}"></i>' if value else 'Seleccionar'}
                </span>
            </a>
        </div>
        '''
        return mark_safe(html)
