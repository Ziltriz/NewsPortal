from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import RemarkablePlace


admin.site.register(RemarkablePlace, LeafletGeoAdmin)

        