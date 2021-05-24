from django.db import models
from django.core.validators import MaxLengthValidator

# Create your models here.

# 税率マスタ
class Tax(models.Model):
    id = models.AutoField(verbose_name='税率ID', primary_key=True)
    rate = models.FloatField(verbose_name='税率')
    description = models.CharField(verbose_name='説明', max_length=256)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = '税率'
        verbose_name_plural = '税率'

# 商品マスタ
class Product(models.Model):
    id = models.AutoField(verbose_name='商品ID', primary_key=True)
    name = models.CharField(verbose_name='商品名', max_length=256)
    price = models.PositiveIntegerField(verbose_name='価格')
    tax = models.ForeignKey(Tax, to_field='id', on_delete=models.SET('削除済み税率'), verbose_name='税率')
    description = models.TextField(verbose_name='商品の説明')
    is_public = models.BooleanField(verbose_name='公開フラグ', default=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name

# 商品画像
class ProductImage(models.Model):
    id = models.AutoField(verbose_name='画像ID', primary_key=True)
    product = models.ForeignKey(Product, to_field='id', on_delete=models.CASCADE, verbose_name='商品')
    path = models.CharField(verbose_name='画像パス', max_length=2048)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name = '商品画像'
        verbose_name_plural = '商品画像'

    def __str__(self):
        return str(self.product)


# 商品オプション
class ProductOption(models.Model):
    id = models.AutoField(verbose_name='オプションID', primary_key=True)
    product = models.ForeignKey(Product, to_field='id', on_delete=models.CASCADE, verbose_name='商品')
    name = models.CharField(verbose_name='オプション名', max_length=256)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '商品オプション'
        verbose_name_plural = '商品オプション'

    def __str__(self):
        return self.name


# 注文
class Order(models.Model):
    id = models.AutoField(verbose_name='注文ID', primary_key=True)
    product = models.ForeignKey(Product, to_field='id', on_delete=models.SET('削除済み商品'), verbose_name='商品')
    product_option = models.ForeignKey(ProductOption, to_field='id', on_delete=models.SET('削除済み商品オプション'), verbose_name='商品オプション', null=True, blank=True)
    payjp_charge_id = models.CharField(verbose_name='PAYJP決済ID', max_length=256, blank=True, null=True)
    buyer_name = models.CharField(verbose_name='購入者氏名', max_length=256)
    buyer_address = models.CharField(verbose_name='購入者住所', max_length=256)
    buyer_zip_code = models.CharField(verbose_name='購入者郵便番号', max_length=10)
    buyer_tel = models.CharField(verbose_name='購入者電話番号', max_length=20)
    buyer_email = models.CharField(verbose_name='購入者メールアドレス', max_length=256)
    payment_amount = models.PositiveIntegerField(verbose_name='支払い金額')
    created_at = models.DateTimeField(verbose_name='購入日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '注文'
        verbose_name_plural = '注文'

    def __str__(self):
        return str(self.created_at.strftime('%Y/%m/%d')) + ' ' + self.product.name


# 注文状態履歴
class OrderStatusHistory(models.Model):

    # 注文状態
    class OrderStatus(models.IntegerChoices):
        FAILED = 0, '注文受付失敗'
        ORDERD = 1, '注文受付済み'
        CANCELED = 2, 'キャンセル済み'
        SHIPPED = 3, '発送済み'

    id = models.AutoField(verbose_name='注文状態変更ID', primary_key=True)
    order = models.ForeignKey(Order, to_field='id', on_delete=models.SET('削除済み注文ID'), verbose_name='注文ID')
    status = models.IntegerField(verbose_name='注文状態', choices=OrderStatus.choices)
    created_at = models.DateTimeField(verbose_name='注文状態変更日時', auto_now_add=True)
        
    class Meta:
        verbose_name = '注文状態履歴'
        verbose_name_plural = '注文状態履歴'

    def __str__(self):
        return self.order.product.name
        