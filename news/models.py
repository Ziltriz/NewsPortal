from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок новости')
    main_image = models.ImageField(upload_to='news_images/', verbose_name='Главное изображение')
    preview_image = models.ImageField(verbose_name='Превью-изображение', editable=False, blank=True, null=True)
    content = models.TextField(verbose_name='Текст новости')
    publication_date = models.DateTimeField(verbose_name='Дата публикации', default=timezone.now)
    author = models.ForeignKey(User, verbose_name='Автор новости', on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if not self.preview_image and self.main_image:
            image = Image.open(self.main_image)
            output_io = BytesIO()
            image.thumbnail((200, 200))
            image.save(output_io, format=image.format)
            self.preview_image.save(
                f"preview_{self.main_image.name}",
                InMemoryUploadedFile(
                    output_io,
                    'ImageField',
                    f"preview_{self.main_image.name}",
                    self.main_image.file.content_type,
                    sys.getsizeof(output_io),
                    None
                )
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    
    

