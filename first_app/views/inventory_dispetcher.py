from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.views.equip import equip
from first_app.views.drop import drop
from first_app.views.draw_world import draw_world

def choicer(request):
    if request.POST['choicer'] == "drop item":
        return drop(request)
    elif request.POST['choicer'] == "equip item":
        return equip(request)
    else:
        return draw_world(request)
