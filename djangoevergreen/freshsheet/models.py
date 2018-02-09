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
# Category Input
# ------------------------------------------------------------------------------


# class Category(models.Model):
#
#     name = models.CharField(
#         max_length=50,
#         default='',
#     )
#
#     def __str__(self):
#         return str(self.name)


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
        default=('LB', 'Pounds'),
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
# Cart Input
# ------------------------------------------------------------------------------


class OrderItem(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    active = models.BooleanField()
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')


class Order(models.Model):

    order_id = models.PositiveIntegerField(
        "Order Number",
        null=True,
        default=None,
        unique=True,
    )

    # def order_total(self, cart, request):
    #     order_total = 0
    #     for OrderItem.item in cart:
    #         OrderItem.price += order_total
    #
    #     sum(OrderItem.price, self).order_total(cart, request)
    #
    # def populate_from_cart(self, cart, request):
    #     super(Order, self).populate_from_cart(cart, request)
    @property
    def price(self):
        return sum([i.price for i in self.items.all()])

# ------------------------------------------------------------------------------
# User Override
# ------------------------------------------------------------------------------


class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

