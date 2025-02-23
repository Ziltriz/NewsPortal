from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import RemarkablePlace, WeatherSummary


admin.site.register(RemarkablePlace, LeafletGeoAdmin)

@admin.register(WeatherSummary)
class WeatherSummaryAdmin(admin.ModelAdmin):
    list_display = ('place', 'timestamp', 'temperature', 'humidity', 'pressure', 'wind_direction', 'wind_speed')
    list_filter = ('place', 'timestamp')  
    search_fields = ('place__name',)
    date_hierarchy = 'timestamp'  
    ordering = ('-timestamp',) 

        