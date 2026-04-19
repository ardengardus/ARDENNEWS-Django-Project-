from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='news')
    pub_date = models.DateTimeField('Дата публикации', default=timezone.now)
    image = models.ImageField('Изображение', upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[str(self.id)])

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    text = models.TextField('Текст комментария')
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']

    def __str__(self):
        return f'Комментарий от {self.author.username}'