from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe
from django.conf import settings
from .models import Product, ProductImage, ProductOption, Tax, Order, OrderStatusHistory

DEFAULT_IMAGE_URL = settings.STATIC_URL + 'img/ec/no_image_gray.png'

# Register your models here.

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = 3

class ProductOptionInline(admin.StackedInline):
    model = ProductOption

class TaxAdmin(admin.ModelAdmin):
    list_display = ['description', 'rate']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionInline, ProductImageInline]
    list_filter = ['is_public', 'updated_at']
    list_display = ['name', 'description', 'product_image', 'is_public', 'updated_at']

    def product_image(self, obj):
        return mark_safe('<img src="{}" style="width:80px; height:80px; object-fit:cover;"'.format(ProductImage.objects.filter(product=obj.id).earliest('updated_at').path))
    product_image.short_description = '商品画像(1)'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', 'buyer_name', 'buyer_tel', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['id']
    actions = ['setStatusForCanceled', 'setStatusForShipped']

    def status(self, obj):
        return OrderStatusHistory.OrderStatus.choices[OrderStatusHistory.objects.filter(order=obj.id).latest('created_at').status][1]
    status.short_description = '注文状態'

    def setStatusForCanceled(self, request, queryset):
        for order in queryset:
            OrderStatusHistory.objects.create(order=order, status=OrderStatusHistory.OrderStatus.CANCELED)
    setStatusForCanceled.short_description = '選択された 注文 の状態を「キャンセル」に変更'

    def setStatusForShipped(self, request, queryset):
        for order in queryset:
            OrderStatusHistory.objects.create(order=order, status=OrderStatusHistory.OrderStatus.SHIPPED)
    setStatusForShipped.short_description = '選択された 注文 の状態を「発送済み」に変更'

class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_at']
    list_filter = ['order', 'status', 'created_at']

admin.site.register(Tax, TaxAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)
