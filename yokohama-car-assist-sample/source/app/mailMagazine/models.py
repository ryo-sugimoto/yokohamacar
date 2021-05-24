from django.db import models

# Create your models here.

# メールマガジン
class MailMagazine(models.Model):

    # 送信状態
    class SendStatus(models.IntegerChoices):
        UNSENT = 0, '未送信'
        SENDED = 1, '送信済み'
        FAILED = 2, '送信失敗'
        UPDATED = 3, '更新後未送信'

    id = models.AutoField(verbose_name='メールマガジンID', primary_key=True)
    title = models.CharField(verbose_name='タイトル', max_length=256)
    body = models.TextField(verbose_name='内容')
    status = models.IntegerField(verbose_name='メールマガジン状態', choices=SendStatus.choices, default=SendStatus.UNSENT)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'メールマガジン'
        verbose_name_plural = 'メールマガジン'

    def __str__(self):
        return self.title

# 購読ユーザー
class SubscribedUser(models.Model):

    id = models.AutoField(verbose_name='購読ユーザーID', primary_key=True)
    name = models.CharField(verbose_name='氏名', max_length=256)
    mail_address = models.CharField(verbose_name='メールアドレス', max_length=256)
    is_subscribe = models.BooleanField(verbose_name='購読状態', default=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '購読ユーザー'
        verbose_name_plural = '購読ユーザー'
    
    def __str__(self):
        return self.name
