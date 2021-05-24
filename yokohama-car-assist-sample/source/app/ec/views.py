import email
from django.conf import settings
from django.db import transaction
from django.views import generic
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from .models import Product, ProductImage, ProductOption, Tax, Order, OrderStatusHistory
from .forms import OrderForm
from pathlib import Path
import environ, math, os, logging, payjp

# Load .env
env = environ.Env()
env.read_env('.env')

DEFAULT_IMAGE_URL = settings.STATIC_URL + 'img/ec/no_image_gray.png'
JSON_KEY_OF_PRODUCT = 'product'
JSON_KEY_OF_PRODUCT_OPTION = 'product_option'
JSON_KEY_OF_PRODUCT_IMAGE = 'product_image'
JSON_KEY_OF_PAYJP_PUBLIC_KEY = 'payjp_public_key'
FIELD_NAME_OF_BUYER_EMAIL = 'buyer_email'
POST_PARAMETER_NAME_OF_PAYJP_TOKEN = 'payjp-token'
PAYJP_CURRENCY='jpy'

# Create your views here.

class ProductListView(generic.ListView):
    model = Product
    template_name = 'ec/product-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_public=True).all().order_by('-updated_at').values()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for product in context.get(self.context_object_name):
            # 商品画像を取得
            product_image = ProductImage.objects.select_related('product').filter(product=product.get('id')).first()
            # 商品画像があればセット、なければデフォルトの画像をセット
            product[JSON_KEY_OF_PRODUCT_IMAGE] = product_image.path if product_image is not None else DEFAULT_IMAGE_URL
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'ec/product.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        product = context.get(JSON_KEY_OF_PRODUCT)
        # 税込み価格を再セット
        product.price = math.ceil(product.price * Tax.objects.get(pk=product.tax_id).rate)
        # 商品画像リストの取得
        path_list = []
        for image in ProductImage.objects.filter(product=product.id).all():
            path_list.append(image.path)
        # 商品画像リストがあればセット、なければデフォルト画像をセット
        context[JSON_KEY_OF_PRODUCT_IMAGE] = path_list if len(path_list) != 0 else [DEFAULT_IMAGE_URL]
        # オプションがあればセット
        options = ProductOption.objects.select_related('product').filter(product=product.id)
        context[JSON_KEY_OF_PRODUCT_OPTION] = options.all() if options.first() is not None else None
        return context

class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'ec/order.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # PAY.JPの公開鍵セット
        context[JSON_KEY_OF_PAYJP_PUBLIC_KEY] = env('PAYJP_PUBLIC_KEY')
        return context

    def get_form(self):
        form = super(OrderCreateView, self).get_form()
        # 商品のセット
        form.fields.get('product').initial = Product.objects.get(pk=self.request.GET.get(JSON_KEY_OF_PRODUCT))
        # 商品オプションがあればセット
        product_option = self.request.GET.get(JSON_KEY_OF_PRODUCT_OPTION)
        form.fields.get('product_option').initial = ProductOption.objects.get(pk=product_option) if product_option is not None else None
        return form
    
    def form_valid(self, form):
        post_data = self.request.POST
        product = Product.objects.get(pk=post_data.get(JSON_KEY_OF_PRODUCT))
        payment_amount = math.ceil(product.price * Tax.objects.get(pk=product.tax_id).rate)

        # モデルの一時保存
        order = form.save(commit=False)
        order.payment_amount = payment_amount

        with transaction.atomic():

            # 注文情報の保存
            order.save()

            try:
                # PAY.JP 顧客情報の送信
                customer = payjp.Customer.create(
                    email=post_data.get(FIELD_NAME_OF_BUYER_EMAIL),
                    card=post_data.get(POST_PARAMETER_NAME_OF_PAYJP_TOKEN))

                # PAY.JP 決済情報の送信
                charge = payjp.Charge.create(
                    amount=payment_amount,
                    currency=PAYJP_CURRENCY,
                    customer=customer.id,
                    description='ご注文ID : '+str(order.id),
                )
                
                # PAY.JPの決済IDをセットしてDB更新
                order.payjp_charge_id = charge.id
                order.save()

                # 注文状態の保存
                OrderStatusHistory.objects.create(
                    order=order,
                    status=OrderStatusHistory.OrderStatus.ORDERD
                )

                return redirect('ec:complete')

            except BaseException as exception:

                # 注文状態の保存
                OrderStatusHistory.objects.create(
                    order=order,
                    status=OrderStatusHistory.OrderStatus.FAILED
                )

                logging.getLogger(__name__).error(exception)

                return redirect('ec:failed')

class OrderCreateCompleteView(generic.TemplateView):
    template_name = 'ec/complete.html'

class OrderCreateFailedView(generic.TemplateView):
    template_name = 'ec/failed.html'