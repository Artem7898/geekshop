
from django.conf import settings
from django.db import models
from mainapp.models import Product
from ordersapp.models import OrderItem


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity +=  object.quantity
#             object.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')


    def save(self, *args, **kwargs):
        if self.pk:
           self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
           self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)


    # @property
    def product_cost(self):
        return self.product.price * self.quantity

    product_cost = property(product_cost)

    # @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    total_quantity = property(total_quantity)

    # @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    total_cost = property(total_cost)

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_product_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        return basket_items_dic

    # def delete(self):
    #     self.product_quantity += self.quantity
    #     self.product.save()

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

    