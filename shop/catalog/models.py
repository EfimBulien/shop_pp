from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_products', kwargs={'category_id': self.pk})

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_products', kwargs={'tag_id': self.pk})

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    #available_quantity = models.PositiveIntegerField(default=0, verbose_name="Доступное количество")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.pk})

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]
    
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    customer_name = models.CharField(max_length=100, verbose_name="ФИО клиента")
    #status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    products = models.ManyToManyField(Product, through='OrderItem', verbose_name="Товары")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return f"Заказ №{self.number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    discount_per_item = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Скидка за единицу")
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity} (заказ {self.order.number})"
    
