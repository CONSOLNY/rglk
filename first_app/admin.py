from django.contrib import admin
from first_app.models import *
# Register your models here.

class CellAdmin(admin.ModelAdmin):
    list_display = ("x", "y")

class CharacterAdmin(admin.ModelAdmin):
    list_display = ("cell", "hp", "name", "defense", "attack")

class MonsterAdmin(admin.ModelAdmin):
    list_display = ("cell", "hp", "name", "defense", "attack")

class LootTypeAdmin(admin.ModelAdmin):
    list_display = ("item",)

class LootAdmin(admin.ModelAdmin):
    list_display = ("item_type", "item_name", "item_stats")

class InventoryCellAdmin(admin.ModelAdmin):
    list_display = ("inv_coord", "inv_content",)

class InventoryCharacterAdmin(admin.ModelAdmin):
    list_display = ("char", "content")

class SlotCharacterAdmin(admin.ModelAdmin):
    list_display = ("slot", "slot_type")

admin.site.register(Cell, CellAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Monster, MonsterAdmin)
admin.site.register(LootType, LootTypeAdmin)
admin.site.register(Loot, LootAdmin)
admin.site.register(InventoryCell, InventoryCellAdmin)
admin.site.register(InventoryCharacter, InventoryCharacterAdmin)
admin.site.register(SlotCharacter, SlotCharacterAdmin)
