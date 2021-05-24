from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging
from .models import MailMagazine, SubscribedUser

# Register your models here.
class MailMagazineAdmin(SummernoteModelAdmin):
    exclude = ['status']
    list_display = ['title', 'status', 'created_at', 'updated_at']
    list_filter = ['status']
    actions = ['send']

    def send(self, request, queryset):
        """
        選択したメールマガジンの送信
        """
        for mailMagazine in queryset:
            try:
                email = EmailMultiAlternatives(mailMagazine.title, mailMagazine.body, settings.EMAIL_HOST_USER, [], MailMagazineAdmin.getAllSubscribedUser())
                email.attach_alternative(mailMagazine.body, "text/html")
                email.send()
                mailMagazine.status = MailMagazine.SendStatus.SENDED
            except BaseException as exception:
                mailMagazine.status = MailMagazine.SendStatus.FAILED
                logging.getLogger(__name__).error(exception)
            finally:
                mailMagazine.save()
    send.short_description = '選択された メールマガジン の送信'

    def getAllSubscribedUser():
        """
        メルマガ購読ユーザーの取得
        """
        recipient_list = []
        for user in SubscribedUser.objects.filter(is_subscribe=True).all():
            recipient_list.append(user.mail_address)
        return recipient_list

    def save_model(self, request, obj, form, change):
        """
        save_modelのオーバーライド
        """
        if (obj.id is not None):
            obj.status = MailMagazine.SendStatus.UPDATED
        super(MailMagazineAdmin, self).save_model(request, obj, form, change)
        

class SubscribedUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'mail_address', 'is_subscribe', 'updated_at']

admin.site.register(MailMagazine, MailMagazineAdmin)
admin.site.register(SubscribedUser, SubscribedUserAdmin)
admin.site.unregister(get_attachment_model())
