from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.views.draw_world import draw_world

def drop(request):
    char = Character.objects.first()
    can_drop_item = InventoryCharacter.objects.filter(char=char).exists()
    if can_drop_item:
        item = InventoryCharacter.objects.filter(char=char).first()
        new_cell = InventoryCell.objects.create(inv_coord=char.cell, inv_content=item.content)
        slot = SlotCharacter.objects.get(slot=item)
        if slot.slot_type.item == 'Weapon':
            attack_stats = slot.slot.content.item_stats
            char.attack -= attack_stats
            slot.slot = None
            slot.save()
            char.save()
        elif slot.slot_type.item == 'Armor':
            defense_stats = slot.slot.content.item_stats
            char.defense -= defense_stats
            slot.slot = None
            slot.save()
            char.save()
    item.delete()
    return draw_world(request)
