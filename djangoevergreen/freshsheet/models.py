from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.

# ------------------------------------------------------------------------------
# Farms Database Input
# ------------------------------------------------------------------------------


class Farm(models.Model):

    # Example: Bloom Creek Cranberries, Little Rock, WA
    name = models.CharField(
        default='',
        max_length=255,
    )

    # Example: ('R', 'red'),
    RIBBON_COLOR = (('R', 'red'),
                    ('OR', 'orange'),
                    ('Y', 'yellow'),
                    ('OL', 'olive'),
                    ('G', 'green'),
                    ('T', 'teal'),
                    ('B', 'blue'),
                    ('V', 'violet'),
                    ('PU', 'purple'),
                    ('PI', 'pink'),
                    ('BR', 'brown'),
                    ('G', 'grey'),
                    ('BL', 'black'),

                    )

    ribbon_color = models.CharField(
        max_length=20,
        choices=RIBBON_COLOR,
        null=True,
        blank=True,
        default='',
    )

    # Example: (555)555-5555
    # Example: 5555555555
    # Example: 555-555-5555
    phone = models.CharField(
        default='',
        max_length=15,
    )

    # Example: example@example.com
    email = models.EmailField(
        default='',
    )

    # Example: ('WA', 'Washington')
    STATE = (('AL', 'Alabama'),
             ('AZ', 'Arizona'),
             ('AR', 'Arkansas'),
             ('CA', 'California'),
             ('CO', 'Colorado'),
             ('CT', 'Connecticut'),
             ('DE', 'Delaware'),
             ('DC', 'District of Columbia'),
             ('FL', 'Florida'),
             ('GA', 'Georgia'),
             ('ID', 'Idaho'),
             ('IL', 'Illinois'),
             ('IN', 'Indiana'),
             ('IA', 'Iowa'),
             ('KS', 'Kansas'),
             ('KY', 'Kentucky'),
             ('LA', 'Louisiana'),
             ('ME', 'Maine'),
             ('MD', 'Maryland'),
             ('MA', 'Massachusetts'),
             ('MI', 'Michigan'),
             ('MN', 'Minnesota'),
             ('MS', 'Mississippi'),
             ('MO', 'Missouri'),
             ('MT', 'Montana'),
             ('NE', 'Nebraska'),
             ('NV', 'Nevada'),
             ('NH', 'New Hampshire'),
             ('NJ', 'New Jersey'),
             ('NM', 'New Mexico'),
             ('NY', 'New York'),
             ('NC', 'North Carolina'),
             ('ND', 'North Dakota'),
             ('OH', 'Ohio'),
             ('OK', 'Oklahoma'),
             ('OR', 'Oregon'),
             ('PA', 'Pennsylvania'),
             ('RI', 'Rhode Island'),
             ('SC', 'South Carolina'),
             ('SD', 'South Dakota'),
             ('TN', 'Tennessee'),
             ('TX', 'Texas'),
             ('UT', 'Utah'),
             ('VT', 'Vermont'),
             ('VA', 'Virginia'),
             ('WA', 'Washington'),
             ('WV', 'West Virginia'),
             ('WI', 'Wisconsin'),
             ('WY', 'Wyoming'),
             )

    state = models.CharField(
        max_length=40,
        choices=STATE,
        null=True,
        blank=False,
        default='WA'
    )

    city = models.CharField(
        default='',
        max_length=100,
    )

    def __str__(self):
        return self.name

# ------------------------------------------------------------------------------
# FoodItem Database Input
# ------------------------------------------------------------------------------


class FoodItem(models.Model):
    # Example: Rainbow Carrot
    name = models.CharField(
        default='',
        max_length=100,
    )

    farm = models.ForeignKey(
        Farm,
        related_name='vegetables',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    category = models.CharField(
        null=True,
        blank=True,
        default='',
        max_length=40,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=''

    )

    # Example: A short description of the vegetable.
    description = models.TextField(
        max_length=400,
        default='',
    )

    FOOD_COLOR = (('R', 'red'),
                  ('OR', 'orange'),
                  ('Y', 'yellow'),
                  ('OL', 'olive'),
                  ('GN', 'green'),
                  ('T', 'teal'),
                  ('B', 'blue'),
                  ('V', 'violet'),
                  ('PU', 'purple'),
                  ('PI', 'pink'),
                  ('BR', 'brown'),
                  ('GR', 'grey'),
                  ('BL', 'black'),
                  ('WH', 'white'),
                  )

    food_color = models.CharField(
        max_length=20,
        choices=FOOD_COLOR,
        null=True,
        blank=True,
        default='',
    )

    # Example: ('LB', 'Pounds'),
    UNIT = (('LB', 'Pound(s)'),
            ('BU', 'Bundle'),
            ('HD', 'Head'),
            ('C', 'Count'),
            )

    unit = models.CharField(
        max_length=15,
        choices=UNIT,
        default=('LB', 'Pound(s)'),
        null=False,
        blank=False,
    )

    # Example: 100
    quantity = models.PositiveIntegerField(
        default=0,
    )

    # Example: 100.00
    price = models.DecimalField(
        default='0.00',
        max_digits=8,
        decimal_places=2,
    )

    def get_unit_verbose(self):
        if self.unit == 'LB':
            return "Pounds"
        if self.unit == 'BU':
            return "Bundles"
        if self.unit == 'HD':
            return "Heads"
        if self.unit == 'C':
            return "Count"

    def __str__(self):
        return self.name

# ------------------------------------------------------------------------------
# Restaurant Database Input
# ------------------------------------------------------------------------------


class Restaurant(models.Model):
    # Example: John Doe
    contact_name = models.CharField(
        default='',
        max_length=100,
    )

    # Example: (555)555-5555
    # Example: 5555555555
    # Example: 555-555-5555
    phone = models.CharField(
        default='',
        max_length=15,
    )

    # Example: Joule
    restaurant_name = models.CharField(
        default='',
        max_length=100,
    )

    # Example: example@example.com
    email = models.EmailField(
        default='',
    )


# ------------------------------------------------------------------------------
# Fresh Sheet Database Input
# ------------------------------------------------------------------------------


class FreshSheet(models.Model):

    items = models.ManyToManyField(FoodItem)

    # Example:
    created_at = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.created_at)

# ------------------------------------------------------------------------------
# Order Model
# ------------------------------------------------------------------------------


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_cost(self):
        return self.price * self.quantity

    def get_unit_verbose(self):
        if self.item.unit == 'LB' and self.quantity >= 2:
            return "Pounds"
        if self.item.unit == 'LB' and self.quantity == 1:
            return "Pound"
        if self.item.unit == 'BU' and self.quantity >= 2:
            return "Bundles"
        if self.item.unit == 'BU' and self.quantity == 1:
            return "Bundle"
        if self.item.unit == 'HD' and self.quantity >= 2:
            return "Heads"
        if self.item.unit == 'HD' and self.quantity == 1:
            return "Head"
        if self.item.unit == 'C':
            return "Count"


class Order(models.Model):
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField('Date', auto_now_add=True)
    status = models.CharField(
        max_length=40,
        null=False,
        blank=False,
        default='Shopping',
        choices=(
            ('P', 'Pending'),
            ('C', 'Complete'),
            ('O', 'Out For Delivery'),
            ('D', 'Delivered')
        ))

    @property
    def order_total_cost(self):
        total_cost = 0
        for item in self.items.all():
            total_cost += item.quantity * item.price
        return total_cost

    def __str__(self):
        return 'Order #' + str(self.pk)


# ------------------------------------------------------------------------------
# User Model
# ------------------------------------------------------------------------------
class User(AbstractUser, models.Model):
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
