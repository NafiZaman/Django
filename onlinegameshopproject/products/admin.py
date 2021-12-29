from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from . models import Product, Stock


class StockAdminConfig(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'platforms', 'in_stock')

    fieldsets = (
        ('Stock Information', {'fields': ('shop',
                                          'product', 'price', 'in_stock')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('shop', 'product', 'price',)
    #     }),
    # )

    # exclude = ('platforms',)


admin.site.register(Product)
admin.site.register(Stock, StockAdminConfig)
