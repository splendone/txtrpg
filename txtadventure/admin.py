from django.contrib import admin

# Register your models here.
from txtadventure.models import Maps,Player,Tiles,Enemies,Items#,ItemTypes

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'wxoid')
admin.site.register(Maps)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Tiles)
admin.site.register(Enemies)
# admin.site.register(ItemTypes)
admin.site.register(Items)
