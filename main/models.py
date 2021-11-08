from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone




class all_posts(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likeCount = models.IntegerField(blank=True, null=True, default=0)
    date = models.DateTimeField(auto_now_add=True)

    is_post = models.BooleanField(default=True)
    CommentCount = models.IntegerField(blank=True, null=True, default=0)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_pinned = models.BooleanField(default=False)


    message = models.CharField(max_length=1000)
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    def __str__(self):
        # if self.is_post:
        return f'[ POST ID : {self.id} ] USER: @{self.owner.username} MESSAGE: {self.message}'
        # else:
        #     return f'[ COMMENT ID : {self.id} / POST ID: {self.parent.id} ] USER: @{self.owner.username} MESSAGE: {self.message}'

class hidden_posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(all_posts, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Скрытый пост'
        verbose_name_plural = 'Скрытые посты'
    def __str__(self):
        return 'HIDDEN_POST ID: '+ str(self.post.id) + '/ Message: ' + str(self.post.message) + '/ FROM_USER ID: ' + str(self.user.id)



class likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(all_posts, on_delete=models.CASCADE, related_name='likes_set')
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
    def __str__(self):
        return 'POST ID: '+ str(self.post.id) + ' / USER ID: ' + str(self.user.id)

class user_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="profile")
    avatar = models.FileField(default='main/static/img/svg/user_logo.svg', upload_to='main/static/media/avatars/')
    background = models.FileField(default='main/static/img/svg/back_img_profil.svg', upload_to='main/static/media/avatars/')

    balance = models.FloatField(default=0.00)
    token_cost = models.FloatField(default=1.00)
    procent = models.FloatField(default=0.0)

    online = models.BooleanField(default=False)
    is_username_changed = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    def __str__(self):
        return 'USER ID: '+ str(self.user.id) + ' / USERNAME: ' + str(self.user.username) + '/ Token'


class PostImage(models.Model):
    post = models.ForeignKey(all_posts, default=None, on_delete=models.CASCADE, related_name='PostImage_set')
    images = models.FileField(upload_to='main/static/media/')

    def __str__(self):
        return str(self.post.id)


class complain(models.Model):
    post = models.ForeignKey(all_posts, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
    def __str__(self):
        return str(self.post.id)

class chat(models.Model):
    user = models.ManyToManyField(User)
    data = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

class message(models.Model):
    id = models.IntegerField(primary_key=True)
    chat = models.ForeignKey(chat, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isReaded = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


