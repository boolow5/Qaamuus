from django.contrib import admin

from dictionary.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Word)
admin.site.register(Comment)
admin.site.register(Reaction)
