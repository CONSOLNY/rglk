from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import *

action_dict = dict()

# TODO: Create file utils, move filters and checkers to utils.py, import utils to views, player template icon
def flag_filter(query_set, filter_set, predicate, flag_f):
    for ind in range(len(query_set)):
        for ind2 in range(len(filter_set)):
            if predicate(query_set[ind], filter_set[ind2]):
                flag_f(query_set[ind])

def check_take_item(c, cs):
    can_take_item = InventoryCell.objects.filter(inv_coord=c.cell).exists()
    print(can_take_item)
    if can_take_item:
        action_dict['take item'] = '<input type="submit" value="take item" form="BoxForm">'

def check_drop_item(c, cs):
    char = Character.objects.first()
    can_drop_item = InventoryCharacter.objects.filter(char=char).exists()
    if can_drop_item:
        action_dict['drop item'] = '/game/drop/'

def check_equip_item(c, cs):
    char = Character.objects.first()
    slots = SlotCharacter.objects.all()
    for slot in slots:
        if slot.slot is None and InventoryCharacter.objects.filter(content__item_type=slot.slot_type).exists():
            action_dict['equip item'] = '<input type="submit" value="equip item" form="InventoryForm">'

def check_unequip_item(c, cs):
    char = Character.objects.first()
    slots = SlotCharacter.objects.all()
    for slot in slots:
        if slot.slot is not None:
            action_dict['unequip item'] = '<input type="submit" value="unequip item" form="EquippedForm">'

def check_border(c, cs):
    max_x = Cell.objects.aggregate(Max('x'))['x__max']
    max_y = Cell.objects.aggregate(Max('y'))['y__max']
    if c.cell.x != 0:
        action_dict['go left'] = '<a href="/game/move/?direct=left">go left</a>'

    if c.cell.y != 0:
        action_dict['go up'] = '<a href="/game/move/?direct=up">go up</a>'

    if c.cell.x != max_x:
        action_dict['go right'] = '<a href="/game/move/?direct=right">go right</a>'

    if c.cell.y != max_y:
        action_dict['go down'] = '<a href="/game/move/?direct=down">go down</a>'


def fill_dict(c, cs):
    '''
    hp - hitpoints
    c - character
    cs - cells
    update action list
    '''
    action_dict.clear()
    check_border(c, cs)
    check_take_item(c, cs)
    check_equip_item(c, cs)
    check_unequip_item(c, cs)
#    check_drop_item(c, cs)

def fill_loot_list():
    inv = InventoryCharacter.objects.all()
    return inv

def fill_box_loot_list():
    inv = InventoryCell.objects.filter(inv_coord=Character.objects.first().cell)
    if len(inv) == 0:
        return None
    return inv

def equipped_list():
    slots = SlotCharacter.objects.all()
    equipped = []
    for slot in slots:
        if slot.slot is not None:
            equipped.append(slot)
    return equipped
