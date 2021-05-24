from django.db import models

# Create your models here.

# 問い合わせ内容
class Contact(models.Model):
    id = models.AutoField(verbose_name='お問い合わせID', primary_key=True)
    name = models.CharField(verbose_name='氏名', max_length=256)
    mail_address = models.CharField(verbose_name='メールアドレス', max_length=256)
    content = models.TextField(verbose_name='問い合わせ内容')
    created_at = models.DateTimeField(verbose_name='問い合わせ日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'お問い合わせ'
        verbose_name_plural = 'お問い合わせ'
    