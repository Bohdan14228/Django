from django.db import models
from django.urls import reverse
# from users.models import User


class Product(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name='Назва')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст статьи')     # blank=True говорит про то что поле может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Час зміни')
    is_published = models.BooleanField(default=True, verbose_name='Публікація')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категорія')
    branding = models.ForeignKey('Branding', on_delete=models.PROTECT, null=True, verbose_name='Бренд')
    saleornew = models.ForeignKey('SaleorNew', on_delete=models.PROTECT, null=True, verbose_name='Знижки або нове',
                                  blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Продукти'
        verbose_name_plural = 'Продукти'
        ordering = ['id']    # сортировка


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=255, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорія'
        ordering = ['id']


class Branding(models.Model):
    objects = None
    name = models.CharField(max_length=255, db_index=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренд'
        ordering = ['id']


class SaleorNew(models.Model):
    objects = None
    name = models.CharField(max_length=255, db_index=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Знижки або нове'
        verbose_name_plural = 'Знижки або нове'
        ordering = ['id']


class PostPhoto(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name='Назва')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, null=True, verbose_name='Товар')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ['product', 'title']


# class BasketQuerySet(models.QuerySet):
#     def total_sum(self):
#         return sum(basket.sum() for basket in self)
#
#     def total_quantity(self):
#         return sum(basket.quantity for basket in self)
#
#
# class Basket(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField(default=0)
#     created_timestamp = models.DateTimeField(auto_now_add=True)
#
#     objects = BasketQuerySet.as_manager()
#
#     def __str__(self):
#         return f"Корзина для {self.user.email} | Продукты {self.product.name}"
#
#     class Meta:
#         verbose_name_plural = 'Корзина'
#         verbose_name = 'Заказ'
#
#     def sum(self):
#         return self.product.price * self.quantity
