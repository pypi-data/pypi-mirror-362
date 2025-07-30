from django.urls import path
from .views import IconSelectorView

app_name = 'bsicon'

urlpatterns = [
    path('icon-selector/', IconSelectorView.as_view(), name='icon_selector'),
]
