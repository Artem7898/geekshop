from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'
    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлено в обработку'),
        (PROCEEDED, 'обработано'),
        (PAID, 'оплачено'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменено'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    status = models.CharField(
        max_length=3, choices=ORDER_STATUSES, default=FORMING, verbose_name='статус')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания заказа')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления заказа')

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='заказ', related_name='orderitems')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='количество')

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk)

    @property
    def product_cost(self):
        return self.product.price * self.quantity


class OrderItemQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)



    






