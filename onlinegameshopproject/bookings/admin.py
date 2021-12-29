from django.contrib import admin
from .models import Booking


class BookingAdminConfig(admin.ModelAdmin):
    list_display = ('stock', 'customer', 'platform',
                    'is_arrived', 'is_picked_up')

    # fieldsets = (
    #     ('Stock Information', {'fields': ('shop',
    #                                       'product', 'price', 'in_stock')}),


admin.site.register(Booking, BookingAdminConfig)
