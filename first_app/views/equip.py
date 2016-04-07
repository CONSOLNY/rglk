from django.db.models import F
from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.utils import *
from first_app.views.draw_world import draw_world

def equip(request):
    item_id = int(request.POST.get("Inventory", -1))
    if item_id == -1:
        return draw_world(request)

    char = Character.objects.first()
    item_for_equip = InventoryCharacter.objects.get(id=item_id)
    slot_for_equip = SlotCharacter.objects.get(slot_type=item_for_equip.content.item_type)
    if slot_for_equip.slot_type.item == 'Weapon':
        slot_for_equip.slot = item_for_equip
        attack_stats = item_for_equip.content.item_stats
        char.attack += attack_stats
    elif slot_for_equip.slot_type.item == 'Armor':
        slot_for_equip.slot = item_for_equip
        defense_stats = item_for_equip.content.item_stats
        char.defense += defense_stats
    slot_for_equip.save()
    char.save()
    return draw_world(request)
