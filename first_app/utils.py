from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.http import urlencode
from django.http import HttpResponse
from django.db.models import Max
from math import sqrt
from first_app.models import *
from first_app.views.landing import landing

action_dict = dict()
template_data_dict = dict()

# TODO: Izmenit drop view, add FIGHTINGS!!!, dead
def flag_filter(query_set, filter_set, predicate, flag_f):
#    for ind in range(len(query_set)):
#        for ind2 in range(len(filter_set)):
#            if predicate(query_set[ind], filter_set[ind2]):
#                flag_f(query_set[ind])
    for obj in query_set:
        for _filter in filter_set:
            if predicate(obj, _filter):
                flag_f(obj)

def mob_attack():
    char = Character.objects.first()
    cur_mob = Monster.objects.get(cell=char.cell)
    damage_taken = cur_mob.attack - char.defense
    if damage_taken < 0:
        char.hp = char.hp
    char.hp -= damage_taken
    char.save()
    dead = False
    if char.hp <= 0:
        char.delete()
        dead = True
    return dead 

def check_take_item(c, cs):
    can_take_item = InventoryCell.objects.filter(inv_coord=c.cell).exists()
    if can_take_item:
        action_dict['take item'] = '<input type="submit" value="take item" form="BoxForm">'

def check_drop_item(c, cs):
    char = Character.objects.first()
    can_drop_item = InventoryCharacter.objects.filter(char=char).exists()
    if can_drop_item:
        action_dict['drop item'] = '<input type="submit" name="choicer" value="drop item" form="InventoryDispetcherForm">'

def check_equip_item(c, cs):
    char = Character.objects.first()
    slots = SlotCharacter.objects.all()
    for slot in slots:
        if slot.slot is None and InventoryCharacter.objects.filter(content__item_type=slot.slot_type).exists():
            action_dict['equip item'] = '<input type="submit" name="choicer" value="equip item" form="InventoryDispetcherForm">'

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

def check_combat(c, cs):
    combat = Monster.objects.filter(cell=c.cell).exists()
    if combat: 
        action_dict['attack'] = '<a href="/game/attack/">attack</a>'

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
    check_drop_item(c, cs)
    check_combat(c, cs)

def fill_loot_list():
    inv = InventoryCharacter.objects.all()
    if len(inv) == 0:
        return None
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

def template_data_fill():
    template_data_dict['list_items'] = fill_loot_list()
    template_data_dict['box_items'] = fill_box_loot_list()
    template_data_dict['equipped_items'] = equipped_list()
