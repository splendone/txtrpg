from django.contrib import admin

# Register your models here
from taxidata.models import Taxi

class TaxiAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'timeField', 'peoples', 'taxies')
    fields = ('location', 'timeField', 'peoples', 'taxies')
    list_filter = ('timeField',)
    pass

admin.site.register(Taxi, TaxiAdmin)