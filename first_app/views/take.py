from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.views.draw_world import draw_world

def take(request):
    item_id = int(request.POST.get("Box", -1))
    if item_id == -1:
        return draw_world(request)

    char = Character.objects.first()
    content = InventoryCell.objects.get(id=item_id).inv_content #TODO sdghsdfhgsdhg
    InventoryCharacter.objects.create(char=char, content=content)
    InventoryCell.objects.get(id=item_id).delete()
    char.save()
    return draw_world(request)
