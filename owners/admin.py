from django.contrib import admin
from .models import Owner , PetType

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','pet_type', 'pet_name', ]
    
admin.site.register(Owner, OwnerAdmin )
admin.site.register(PetType)
