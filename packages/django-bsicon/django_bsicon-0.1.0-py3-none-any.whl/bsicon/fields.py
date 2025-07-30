from django.db import models
from .widgets import BsIconWidget

class BsIconField(models.CharField):
    description = "Campo para iconos de Bootstrap"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = BsIconWidget
        return super().formfield(**kwargs)
