from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import * 
from first_app.utils import *

def draw_world(request):
    def pos_predicate(arg1, arg2):
        return arg1.x == arg2.cell.x and arg1.y == arg2.cell.y
    
    def invpos_predicate(arg1, arg2):
        return arg1.x == arg2.inv_coord.x and arg1.y == arg2.inv_coord.y

    def player_flag(arg1):
        arg1.type = "player"

    def mob_flag(arg1):
        arg1.type = "mob"

    def inv_flag(arg1):
        arg1.type = "inv"

    def equip_flag(arg1):
        arg1.type = "equip"

    cells = Cell.objects.all()

    char = Character.objects.all()

    mob = Monster.objects.all()

    inv = InventoryCell.objects.all()

    flag_filter(cells, char, pos_predicate, player_flag)
    flag_filter(cells, mob, pos_predicate, mob_flag)
    flag_filter(cells, inv, invpos_predicate, inv_flag)

    data = []
    # TODO: добавить вьюхи чтобы одевать/снимать слот оружия/брони, выкидывать предметы, использовать item_type potions, FIGHTS!!!, dead
    fill_dict(char[0], cells)
    for y in range(9):
        tmp = []
        for x in range(9):
            cell = list(filter(lambda c: c.x == x and c.y == y, cells))[0]
            tmp.append(cell)
        data.append(tmp)

    return render(request, 'world.html', context={
        "field": data, 
        "player": char[0], 
        "actions": action_dict,
        "list_items": fill_loot_list(),
        "box_items": fill_box_loot_list(),
        "equipped_items": equipped_list()
    })
