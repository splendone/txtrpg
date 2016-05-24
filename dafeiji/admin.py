from django.contrib import admin

from dafeiji.models import Biaoqing, Pilot, Battle
# Register your models here.
class BiaoqingAdmin(admin.ModelAdmin):
    list_display = ('name', 'seq')

class PilotAdmin(admin.ModelAdmin):
    list_display = ('status', 'best', 'battle')

class BattleAdmin(admin.ModelAdmin):
    list_display = ('win', 'enflight', 'myflight', 'fires')
admin.site.register(Biaoqing, BiaoqingAdmin)
admin.site.register(Pilot, PilotAdmin)
admin.site.register(Battle, BattleAdmin)
