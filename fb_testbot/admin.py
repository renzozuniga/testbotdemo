from django.contrib import admin

# Register your models here.
from .models import UsersBot
from .models import Conversations
from .models import FavoriteSongs

admin.site.register(UsersBot)
admin.site.register(Conversations)
admin.site.register(FavoriteSongs)
