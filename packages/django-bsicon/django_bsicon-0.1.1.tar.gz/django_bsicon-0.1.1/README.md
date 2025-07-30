## Installation
```bash
pip install django-bsicon
```

1. Add to INSTALLED_APPS:

```python 
INSTALLED_APPS = [
    ...
    'bsicon',
]
```

2. Use in your models:

```python 
from bsicon.fields import BsIconField

class MyModel(models.Model):
    icon = BsIconField()
```

3. Updating Icons (Optional) / Generate metadata

```bash
python scripts/update_icons.py
```