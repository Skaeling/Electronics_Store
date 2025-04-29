from django.db import models


class NetworkNode(models.Model):
    LEVELS_CHOICES = [
        (0, 'Производитель'),
        (1, 'Контрагент'),
        (2, 'Покупатель'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название')
    purchase_level = models.PositiveIntegerField(choices=LEVELS_CHOICES, verbose_name='Уровень')
    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='consumers',
                                 verbose_name="Поставщик")
    debt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0.00,
                               verbose_name="Задолженность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объект сети'
        verbose_name_plural = 'Объекты сети'


class Contact(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    country = models.CharField(max_length=50, verbose_name="Страна")
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")
    building_number = models.CharField(max_length=10, verbose_name="Номер дома")
    network_node = models.OneToOneField(NetworkNode, on_delete=models.CASCADE, related_name='contacts',
                                        verbose_name="Объект сети")

    def __str__(self):
        return f'{self.email}({self.country})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    model = models.CharField(max_length=50, verbose_name="Модель")
    distributors = models.ManyToManyField(NetworkNode, blank=True, related_name='products',
                                          verbose_name='Дистрибьюторы')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
