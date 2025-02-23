from django.urls import path
from .views import ImportPlacesFromXLSXView, ExportWeatherSummaryView


urlpatterns = [
    path('import-places/', ImportPlacesFromXLSXView.as_view(), name='import_places'),
    path('export-weather/', ExportWeatherSummaryView.as_view(), name='export_weather'),
]