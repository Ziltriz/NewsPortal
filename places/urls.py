from django.urls import path
from .views import ImportPlacesFromXLSXView


urlpatterns = [
    path('import-places/', ImportPlacesFromXLSXView.as_view(), name='import_places'),
]