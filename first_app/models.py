from django.db import models
from django.conf import settings

# Create your models here.

class Cell(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return "{},{}".format(self.x, self.y)

class Character(models.Model):
    cell = models.ForeignKey(Cell, verbose_name="Coordinates")
    hp = models.IntegerField(verbose_name="Hitpoints")
    name = models.CharField(max_length=20)
    defense = models.IntegerField()
    attack = models.IntegerField()
    def __str__(self):
        return "{}".format(self.name)

class Monster(models.Model):
    cell = models.ForeignKey(Cell, verbose_name="Coordinates")
    hp = models.IntegerField(verbose_name="Hitpoints")
    name = models.CharField(max_length=20)
    defense = models.IntegerField()
    attack = models.IntegerField()
    def __str__(self):
        return "{}".format(self.name)

class LootType(models.Model):
    item = models.CharField(max_length=10, verbose_name="Type of item")
    def __str__(self):
        return "{}".format(self.item)

class Loot(models.Model):
    item_type = models.ForeignKey(LootType, verbose_name="Item type")
    item_name = models.CharField(max_length=15, verbose_name="Item name")
    item_stats = models.IntegerField(verbose_name="Item stats")
    def __str__(self):
        return "{},{},{}".format(self.item_type, self.item_name, self.item_stats)

class InventoryCell(models.Model):
    inv_coord = models.ForeignKey(Cell, verbose_name="Loot box coordinates")
    inv_content = models.ForeignKey(Loot, verbose_name="Loot box content")
    def __str__(self):
        return "{},{}".format(self.inv_coord, self.inv_content)

class InventoryCharacter(models.Model):
    char = models.ForeignKey(Character, verbose_name="Character")
    content = models.ForeignKey(Loot, verbose_name="Inventory content")
    def __str__(self):
        return "{},{}".format(self.char, self.content)

class SlotCharacter(models.Model):
    slot = models.ForeignKey(InventoryCharacter, null=True, blank=True, verbose_name="Character slot content")
    slot_type = models.ForeignKey(LootType, verbose_name="Slot type")
    def __str__(self):
        return "{},{}".format(self.slot, self.slot_type)
