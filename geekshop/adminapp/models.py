from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(on_delete=models.CASCADE, to="mainapp.ProductCategory"),
    name = models.CharField(max_length=128, verbose_name="имя продукта"),
    image = models.ImageField(blank=True, upload_to=" products_images "),
    short_desc = models.CharField(blank=True, max_length=60, verbose_name="краткое описание продукта"),
    description = models.TextField(blank=True, verbose_name="описание продукта "),
    price = models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name="цена продукта "),
    quantity = models.PositiveIntegerField(default=0, verbose_name=" количество на складе "),
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f'{self.name}({self.category.name})'



