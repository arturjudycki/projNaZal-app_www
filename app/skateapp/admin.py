from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from .models import Competition, User_detail, Registration

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'date', 'description')
    list_filter = ('city', 'date')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['status', 'id_competition', 'id_user']
    list_filter = ['status', 'id_competition']

admin.site.register(User_detail)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Registration, RegistrationAdmin)


