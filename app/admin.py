from django.contrib import admin
from .models import Item, Expense, ExpenseMethod


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_items', 'amount', 'expense_method', 'user', 'entry_date', 'last_update_date')

    def display_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])

    display_items.short_description = 'Items'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

class ExpenseMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance', 'user', 'entry_date', 'last_update_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'entry_date', 'last_update_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseMethod, ExpenseMethodAdmin)