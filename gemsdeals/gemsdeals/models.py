from django.db import models


# Create your models here.
class Gem(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Customer(models.Model):
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gem = models.ForeignKey(Gem, on_delete=models.CASCADE)
    cost = models.FloatField()
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return 'Сделка №' + str(self.id)

class Menu(models.Model):
    name = models.CharField('Название', max_length=100)
    url = models.CharField('Ссылка', max_length=255)
    position = models.PositiveIntegerField('Позиция', default=1)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('position',)
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
