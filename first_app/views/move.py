from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.views.draw_world import draw_world

def move(request):
    dx = 0
    dy = 0 
    char = Character.objects.first()

    cells = Cell.objects.all()
    max_x = cells.aggregate(Max('x'))['x__max']
    max_y = cells.aggregate(Max('y'))['y__max']

    cur_x = char.cell.x
    cur_y = char.cell.y

    if request.GET['direct'] == 'down':
        dy = 1
    if request.GET['direct'] == 'up':
        dy = -1
    if request.GET['direct'] == 'left':
        dx = -1
    if request.GET['direct'] == 'right':
        dx = 1

    cell = list(filter(lambda t: t.x == char.cell.x + dx and t.y == char.cell.y + dy, cells))
    if len(cell) == 0:
        return draw_world(request)

    cell = cell[0]
    char.cell = cell
    char.save()

    return draw_world(request)
