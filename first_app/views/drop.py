from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.views.draw_world import draw_world

def drop(request):
    item_id = int(request.POST.get("Inventory", -1))
    if item_id == -1:
        return draw_world(request)

    char = Character.objects.first()
    item_for_drop = InventoryCharacter.objects.get(char=char, id=item_id)
    new_cell = InventoryCell.objects.create(inv_coord=char.cell, inv_content=item_for_drop.content)
    slot_for_drop_exists = SlotCharacter.objects.filter(slot=item_for_drop).exists()
    if slot_for_drop_exists:
        slot_for_drop = SlotCharacter.objects.get(slot=item_for_drop)
        if slot_for_drop.slot_type.item == 'Weapon':
            attack_stats = slot_for_drop.slot.content.item_stats
            char.attack -= attack_stats
            slot_for_drop.slot = None
            slot_for_drop.save()
        elif slot_for_drop.slot_type.item == 'Armor':
            defense_stats = slot_for_drop.slot.content.item_stats
            char.defense -= defense_stats
            slot_for_drop.slot = None
            slot_for_drop.save()
    char.save()
    item_for_drop.delete()
    return draw_world(request)
