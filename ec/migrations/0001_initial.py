# Generated by Django 3.2 on 2021-05-23 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='注文ID')),
                ('payjp_charge_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='PAYJP決済ID')),
                ('buyer_name', models.CharField(max_length=256, verbose_name='購入者氏名')),
                ('buyer_address', models.CharField(max_length=256, verbose_name='購入者住所')),
                ('buyer_zip_code', models.CharField(max_length=10, verbose_name='購入者郵便番号')),
                ('buyer_tel', models.CharField(max_length=20, verbose_name='購入者電話番号')),
                ('buyer_email', models.CharField(max_length=256, verbose_name='購入者メールアドレス')),
                ('payment_amount', models.PositiveIntegerField(verbose_name='支払い金額')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='購入日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '注文',
                'verbose_name_plural': '注文',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='商品ID')),
                ('name', models.CharField(max_length=256, verbose_name='商品名')),
                ('price', models.PositiveIntegerField(verbose_name='価格')),
                ('description', models.TextField(verbose_name='商品の説明')),
                ('is_public', models.BooleanField(default=True, verbose_name='公開フラグ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='税率ID')),
                ('rate', models.FloatField(verbose_name='税率')),
                ('description', models.CharField(max_length=256, verbose_name='説明')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '税率',
                'verbose_name_plural': '税率',
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='オプションID')),
                ('name', models.CharField(max_length=256, verbose_name='オプション名')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec.product', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品オプション',
                'verbose_name_plural': '商品オプション',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='画像ID')),
                ('path', models.CharField(max_length=2048, verbose_name='画像パス')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec.product', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品画像',
                'verbose_name_plural': '商品画像',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.ForeignKey(on_delete=models.SET('削除済み税率'), to='ec.tax', verbose_name='税率'),
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='注文状態変更ID')),
                ('status', models.IntegerField(choices=[(0, '注文受付失敗'), (1, '注文受付済み'), (2, 'キャンセル済み'), (3, '発送済み')], verbose_name='注文状態')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='注文状態変更日時')),
                ('order', models.ForeignKey(on_delete=models.SET('削除済み注文ID'), to='ec.order', verbose_name='注文ID')),
            ],
            options={
                'verbose_name': '注文状態履歴',
                'verbose_name_plural': '注文状態履歴',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=models.SET('削除済み商品'), to='ec.product', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET('削除済み商品オプション'), to='ec.productoption', verbose_name='商品オプション'),
        ),
    ]
