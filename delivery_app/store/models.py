from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.formfields import PhoneNumberField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('клиент', 'клиент'),
        ('курьер', 'курьер'),
        ('владелец', 'владелец'),

    )
    user_role = models.CharField(max_length=18, choices=ROLE_CHOICES, default='клиент')
    phone_number = PhoneNumberField(region='KG')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return self.category_name


class Store(models.Model):
    store_name = models.CharField(max_length=32)
    store_image = models.ImageField(upload_to='store_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    address = models.CharField(max_length=32)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name} - {self.address}'

    def get_avg_rating(self):
        ratings = self.store_reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        total = self.store_reviews.all()
        if total.exists():
            if total .count() > 3:
                return '3+'
            return total.count()
        return 0

    def get_count_good_grade(self):
        total = self.store_reviews.all()
        if total.exists():
            num = 0
            for i in total:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100) / total.count())}%'
        return '0%'


class StoreReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='store_reviews',  on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i))for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.client} - {self.store} - {self.rating}'


class ContactInfo(models.Model):
    contact_info = PhoneNumberField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contact_info')

    def __str__(self):
        return f'{self.store} - {self.contact_info}'


class Product(models.Model):
    product_name = models.CharField(max_length=32)
    product_image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    price = models.PositiveIntegerField()
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    category = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f'{self.product_name} - {self.price}'


class ProductCombo(models.Model):
    combo_name = models.CharField(max_length=32)
    combo_image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    price = models.PositiveIntegerField()
    store = models.ForeignKey(Store, related_name='combos', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.combo_name} - {self.store}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        return total_price


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.quantity}'


class Order(models.Model):
    client = models.ForeignKey(UserProfile, related_name='order_client',  on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('ожидает обработки', 'Ожидает обработки'),
        ('в процессе доставки', 'в процессе доставки'),
        ('доставлен', 'Доставлен'),
        ('отменен', 'Отменен')
    )

    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='ожидает обработки')
    delivery_address = models.CharField(max_length=64)
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client} - {self.status} - {self.courier}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, related_name='courier', on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    TYPE_STATUS_CHOICES = (
        ('занят', 'занят'),
        ('доступен', 'доступен'),
    )
    status = models.CharField(max_length=32, choices=TYPE_STATUS_CHOICES)

    def __str__(self):
        return f'{self.user} - {self.status}'


class CourierReview(models.Model):
    client = models.ForeignKey(UserProfile, related_name='client_review', on_delete=models.CASCADE)
    courier = models.ForeignKey(UserProfile, related_name='courier_review', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.rating} - {self.courier}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)








