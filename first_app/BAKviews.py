from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.utils import *
action_dict = dict()

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def check_border(c, cs):
    max_x = Cell.objects.aggregate(Max('x'))['x__max']
    max_y = Cell.objects.aggregate(Max('y'))['y__max']
    if c.cell.x != 0:
        action_dict['go left'] = '/game/move/?direct=left'

    if c.cell.y != 0:
        action_dict['go up'] = '/game/move/?direct=up'

    if c.cell.x != max_x:
        action_dict['go right'] = '/game/move/?direct=right'

    if c.cell.y != max_y:
        action_dict['go down'] = '/game/move/?direct=down'

# TODO: Create file utils, move filters and checkers to utils.py, import utils to views, player template icon
def flag_filter(query_set, filter_set, predicate, flag_f):
    for ind in range(len(query_set)):
        for ind2 in range(len(filter_set)):
            if predicate(query_set[ind], filter_set[ind2]):
                flag_f(query_set[ind])

def check_health(c, cs):
    can_take_item = HP.objects.filter(cell=c.cell).exists()
    if can_take_item:
        action_dict['take item'] = '/game/take/'

def fill_dict(c, cs):
    '''
    hp - hitpoints
    c - character
    cs - cells
    update action list
    '''
    action_dict.clear()
    check_border(c, cs)
    check_health(c, cs)

def draw_world(request):
    def pos_redicate(arg1, arg2):
        return arg1.x == arg2.cell.x and arg1.y == arg2.cell.y

    def player_flag(arg1):
        arg1.type = "player"

    def hearth_flag(arg1):
        arg1.type = "hearth"

    cells = Cell.objects.all()

    char = Character.objects.all()
    flag_filter(cells, char, pos_redicate, player_flag)

    hearths = HP.objects.all()
    flag_filter(cells, hearths, pos_redicate, hearth_flag)

    data = []
    # TODO: Получить игрока, get hp, получить клетку, взять px py
    fill_dict(char[0], cells)
    for y in range(9):
        tmp = []
        for x in range(9):
            cell = list(filter(lambda c: c.x == x and c.y == y, cells))[0]
            tmp.append(cell)
        data.append(tmp)

    return render(request, 'world.html', context={"field": data, "player": char[0], "actions": action_dict})

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

def take(request):
    hp = HP.objects.all()
    char = Character.objects.first()
    cells = Cell.objects.all()
    cur_x = char.cell.x
    cur_y = char.cell.y
    for i in range(len(hp)):
        if cur_x == hp[i].cell.x and cur_y == hp[i].cell.y:
            char.hp += hp[i].hp
            char.save()
            hp[i].delete()
    return draw_world(request)
