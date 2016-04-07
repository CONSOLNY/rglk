from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.utils import *
from first_app.views.draw_world import draw_world

def unequip(request):
    item_id = int(request.POST.get("Equipped", -1))
    if item_id == -1:
        return draw_world(request)
    char = Character.objects.first()
    slot = SlotCharacter.objects.get(slot=InventoryCharacter.objects.get(id=item_id))
    if slot.slot_type.item == 'Weapon':
        attack_stats = slot.slot.content.item_stats
        char.attack -= attack_stats
    elif slot.slot_type.item == 'Armor':
        defense_stats = slot.slot.content.item_stats
        char.defense -= defense_stats
    slot.slot = None
    slot.save()
    char.save() 
    return draw_world(request)
