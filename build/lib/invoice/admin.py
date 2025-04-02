from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'category', 'price', 'quantity', 'discount', 'total_price', 'date')

    def item_name(self, obj):
        return obj.item.name  # Display item name instead of object reference

    item_name.short_description = "Item Name"  # Change column header in the admin panel

admin.site.register(Invoice, InvoiceAdmin)