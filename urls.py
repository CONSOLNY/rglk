"""test_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from first_app.views.draw_world import *
from first_app.views.move import *
from first_app.views.take import *
from first_app.views.drop import *
from first_app.views.equip import *
from first_app.views.unequip import *
from first_app.views.inventory_dispetcher import choicer
from first_app.views.landing import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^game/inventory_dispetcher/', choicer),
    url(r'^game/equip/', equip),
    url(r'^game/unequip/', unequip),
    url(r'^game/take/', take),
    url(r'^game/drop/', drop),
    url(r'^game/move/', move),
    url(r'^game/', draw_world),
    url(r'^', welcome),
]
