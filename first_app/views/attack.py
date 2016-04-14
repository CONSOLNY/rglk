from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from first_app.models import * 
from first_app.views.draw_world import draw_world
from first_app.views.landing import landing

def attack(request):
    char = Character.objects.first()
    mob = Monster.objects.get(cell=char.cell)
    damage_given = char.attack - mob.defense
    if damage_given < 0:
        mob.hp = mob.hp
    else:
        mob.hp -= damage_given
    char.save()
    mob.save()
    if mob.hp <= 0:
        mob.delete()
        char.save()
        return draw_world(request)
    elif char.hp <= 0:
        char.delete()
        mob.delete()
        return landing(request)
    else:
        return draw_world(request)
