from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from first_app.models import *
# Register your models here.

class CellAdmin(admin.ModelAdmin):
    list_display = ("x", "y")

class CharacterAdmin(admin.ModelAdmin):
    list_display = ("cell", "hp", "name", "defense", "attack")

class MonsterAdmin(admin.ModelAdmin):
    list_display = ("cell", "hp", "name", "defense", "attack")

class LootTypeAdmin(admin.ModelAdmin):
    list_display = ("item",)

class LootAdmin(admin.ModelAdmin):
    list_display = ("item_type", "item_name", "item_stats")

class InventoryCellAdmin(admin.ModelAdmin):
    list_display = ("inv_coord", "inv_content",)

class InventoryCharacterAdmin(admin.ModelAdmin):
    list_display = ("char", "content")

class SlotCharacterAdmin(admin.ModelAdmin):
    list_display = ("slot", "slot_type")

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = Player
        fields = ('name',)
    def clean_password2(self):
         password1 = self.cleaned_data.get('password1')
         password2 = self.cleaned_data.get('password2')
         if password1 and password2 and password1 != password2:
             raise forms.ValidationError("Passwords don't match")
         return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Player
        fields = ('name', 'password', 'is_active', 'is_admin')
    def clean_password(self):
        return self.initial['password']

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('name', 'char_list', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = ((None, {'fields': ('name', 'password')}), ('Permissions', {'fields': ('is_admin',)}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('name', 'password1', 'password2')}),)
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ()

admin.site.register(Cell, CellAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Monster, MonsterAdmin)
admin.site.register(LootType, LootTypeAdmin)
admin.site.register(Loot, LootAdmin)
admin.site.register(InventoryCell, InventoryCellAdmin)
admin.site.register(InventoryCharacter, InventoryCharacterAdmin)
admin.site.register(SlotCharacter, SlotCharacterAdmin)
admin.site.register(Player, UserAdmin)
admin.site.unregister(Group)
