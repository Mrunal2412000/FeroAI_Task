from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Product, Order
from django.contrib import messages

# Register your models here.
class userAdmin(UserAdmin):
    list_display = ('id','username')
    search_fields = ('username','email')
    list_per_page = 15

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock_quantity')
    search_fields = ('name', 'description')
    list_per_page = 15

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'order_status', 'address')
    list_filter = ('order_status',)
    search_fields = ('user__username', 'address')
    readonly_fields = ('user','products','delivery_attempt_count')

    def save_model(self, request, obj, form, change):

        if change:
            if obj.order_status =="cancelled" or obj.order_status == "delivered":
                return
            if obj.order_status =="delivery_attempted":
                obj.delivery_attempt_count += 1
                obj.save()
                if obj.delivery_attempt_count > 2:
                    obj.order_status = "cancelled"
                    obj.save()
                    self.message_user(request, 
                    "Tried 2 times delivery failed. {obj} cancelled".format(
                        obj=obj), 
                    level='ERROR')
                return

            original_order_status = Order.objects.get(pk=obj.pk).order_status

            original_index = list(dict(Order.ORDER_STATUS_CHOICES).keys()).index(original_order_status)
            
            new_index = list(dict(Order.ORDER_STATUS_CHOICES).keys()).index(obj.order_status)

            if new_index < original_index and obj.order_status != "delivered":
                self.message_user(request, 
                    "Cannot change order_status from {original} to {new}".format(
                        original=original_order_status, 
                        new=obj.order_status), 
                    level='ERROR')
                return

        super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)

admin.site.register(User,userAdmin)
admin.site.register(Product,ProductAdmin)