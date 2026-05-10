from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='İsim')

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    PRICE_CHOICES = [
        ('€', '€ - Ekonomik'),
        ('€€', '€€ - Orta'),
        ('€€€', '€€€ - Lüks'),
    ]

    name = models.CharField(max_length=200, verbose_name='İsim')
    description = models.TextField(verbose_name='Açıklama')
    address = models.CharField(max_length=300, verbose_name='Adres')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    price_range = models.CharField(
        max_length=3,
        choices=PRICE_CHOICES,
        default='€€',
        verbose_name='Fiyat Aralığı',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurants',
        verbose_name='Kategori',
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_restaurants',
        verbose_name='Oluşturan',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Restoran'
        verbose_name_plural = 'Restoranlar'

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        total = sum(r.stars for r in reviews)
        return round(total / reviews.count(), 1)


class MenuItem(models.Model):
    name = models.CharField(max_length=200, verbose_name='İsim')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Fiyat')
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='Restoran',
    )

    class Meta:
        verbose_name = 'Menü Öğesi'
        verbose_name_plural = 'Menü Öğeleri'

    def __str__(self):
        return f'{self.name} - {self.price}₺'


class Review(models.Model):
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Yıldız',
    )
    comment = models.TextField(verbose_name='Yorum')
    date = models.DateField(auto_now_add=True, verbose_name='Tarih')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Kullanıcı',
        null=True,
        blank=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Restoran',
    )

    class Meta:
        verbose_name = 'Değerlendirme'
        verbose_name_plural = 'Değerlendirmeler'
        ordering = ['-date']

    def __str__(self):
        return f'{self.restaurant.name} - {self.stars} yıldız'
