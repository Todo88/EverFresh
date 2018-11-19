from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from datetime import datetime, timedelta

# Create your models here.

# ------------------------------------------------------------------------------
# Farms Database Input
# ------------------------------------------------------------------------------
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone
from django.utils.timezone import now
from quickbooks.objects import Account


class Farm(models.Model):
    # Example: Bloom Creek Cranberries, Little Rock, WA
    name = models.CharField(
        default='',
        max_length=255,
    )

    # Example: (555)555-5555
    # Example: 5555555555
    # Example: 555-555-5555
    phone = models.CharField(
        default='',
        max_length=15,
        blank=True,
        null=True
    )

    # Example: example@example.com
    email = models.EmailField(
        default='',
        blank=True,
        null=True
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
        blank=True,
        default='WA'
    )

    city = models.CharField(
        default='',
        max_length=100,
        blank=True,
        null=True
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

    featured = models.BooleanField(
        default=False,
        null=False,
        blank=False,
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

    # Example: A short description of the vegetable.
    description = models.TextField(
        max_length=400,
        default='',
        blank=True,
        null=True,
    )

    unit = models.CharField(
        max_length=15,
        default='lb',
        null=False,
        blank=False,
    )

    # Example: 100
    quantity = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )

    # Example: 100.00
    price = models.DecimalField(
        default='0.00',
        max_digits=5,
        decimal_places=2,
        verbose_name="Price"
    )

    case_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Minimum quantity for case price")

    case_price = models.DecimalField(
        default=None,
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
        verbose_name="Case Price"
    )

    wholesale_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Minimum quantity for wholesale price")

    wholesale_price = models.DecimalField(
        default=None,
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
        verbose_name="Wholesale Price"
    )

    account = models.CharField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Account",
        max_length=20
    )

    type = models.CharField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Type",
        max_length=20
    )

    date_added = models.DateField(auto_now_add=True)

    def get_unit_verbose(self):
        if self.unit == 'LB' or self.unit == 'lb' or self.unit == 'Pound' or self.unit == 'pound':
            return "Pounds"
        if self.unit == 'BU' or self.unit == 'bu' or self.unit == 'Bundle' or self.unit == 'bundle':
            return "Bundles"
        if self.unit == 'HD':
            return "Heads"
        if self.unit == 'Head':
            return 'Heads'
        if self.unit == 'C':
            return "Count"
        if self.unit == 'QP':
            return "Quarter Pounds"
        if self.unit == 'Quarter Pound':
            return 'Quarter Pounds'
        if self.unit == 'Ten Count':
            return 'Ten Counts'
        if self.unit == '20CTs':
            return "Twenty Counts"
        else:
            return self.unit

    def get_unit_succinct(self):
        if self.unit == 'lb' or self.unit == 'Pound' or self.unit == 'pound':
            return 'LB'
        if self.unit == 'bu' or self.unit == 'Bundle' or self.unit == 'bundle':
            return 'BU'
        if self.unit == 'Head':
            return 'HD'
        if self.unit == 'Count':
            return 'CT'
        if self.unit == 'Quarter Pound':
            return 'Q LB'
        if self.unit == 'Ten Count':
            return '10 CT'
        if self.unit == 'Twenty Count':
            return '20 CT'
        else:
            return self.unit

    @property
    def is_new(self):
        return self.date_added > (now().date() - timedelta(days=14))

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
    greeting = models.TextField()
    items = models.ManyToManyField(FoodItem)

    # Example:
    created_at = models.DateField(default=datetime.now, blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.created_at)

    def save(self, **kwargs):
        if self.published:
            self.published_at = timezone.now()

            for user in User.objects.all():
                html_message = loader.render_to_string('freshsheet/details.html', {'freshsheet': self})

                send_mail(
                    'test',
                    'test content',
                    user.email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                    html_message=html_message
                )

        return super().save(**kwargs)


# ------------------------------------------------------------------------------
# Order Model
# ------------------------------------------------------------------------------


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_cost(self):
        if self.item.wholesale_count and self.quantity >= self.item.wholesale_count:
            return self.item.wholesale_price * self.quantity
        elif self.item.case_count and self.quantity >= self.item.case_count:
            return self.item.case_price * self.quantity
        else:
            return self.item.price * self.quantity

    @property
    def unit_cost(self):
        """Based on quantity/wholesale prices"""
        if self.item.wholesale_count and self.quantity >= self.item.wholesale_count:
            return self.item.wholesale_price
        if self.item.case_count and self.item.case_count <= self.quantity:
            return self.item.case_price

        return self.item.price

    def get_unit_verbose(self):
        if self.item.unit == 'lb' and self.quantity >= 2:
            return "Pounds"
        if self.item.unit == 'lb' and self.quantity == 1:
            return "Pound"
        if self.item.unit == 'bu' and self.quantity >= 2:
            return "Bundles"
        if self.item.unit == 'bu' and self.quantity == 1:
            return "Bundle"
        if self.item.unit == 'hd' and self.quantity >= 2:
            return "Heads"
        if self.item.unit == 'hd' and self.quantity == 1:
            return "Head"
        if self.item.unit == 'c':
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
            total_cost += item.total_cost
        return total_cost

    def send_to_quickbooks(self, request):
        from quickbooks import QuickBooks, Oauth2SessionManager
        from quickbooks.objects import (Invoice, SalesItemLineDetail, SalesItemLine, Ref)
        from quickbooks.objects.item import Item

        customer = Ref()
        customer.value = 1
        customer.name = self.created_by.get_full_name()
        customer.type = 'Customer'

        account = Account()

        line_items = []

        session_manager = Oauth2SessionManager(
            client_id=settings.QUICKBOOKS_CLIENT_ID,
            client_secret=settings.QUICKBOOKS_CLIENT_SECRET,
            access_token=request.user.qb_access_token,
            refresh_token=request.user.qb_refresh_token,
        )

        session_manager.start_session()

        client = QuickBooks(
            sandbox=True,
            session_manager=session_manager,
            consumer_key=settings.QUICKBOOKS_CLIENT_ID,
            consumer_secret=settings.QUICKBOOKS_CLIENT_SECRET,
            company_id=settings.QUICKBOOKS_COMPANY_ID,
        )

        for item in self.items.all():
            item_lookup = Item.where(f"Name = '{item.item.name}'", qb=client)

            if item_lookup:
                product = item_lookup[0]
            else:
                product = Item()
                product.Name = item.item.name
                product.UnitPrice = item.unit_cost
                product.Type = 'Inventory'
                product.IncomeAccountRef = Account.where("AccountType = 'Income'", qb=client)[0].to_ref()
                product.save(qb=client)

            line_detail = SalesItemLineDetail()
            line_detail.ItemRef = product.to_ref()
            line_detail.UnitPrice = item.unit_cost  # in dollars
            line_detail.Qty = item.quantity  # quantity can be decimal
            line_detail.ServiceDate = now().date().isoformat()

            line = SalesItemLine()
            line.Id = '1'
            line.Amount = item.total_cost  # in dollars
            line.Description = item.item.name
            line.SalesItemLineDetail = line_detail

            line_items.append(line)

        invoice = Invoice()
        invoice.CustomerRef = customer
        invoice.Line = line_items

        invoice.save(qb=client)

    def __str__(self):
        return 'Order #' + str(self.pk)


# ------------------------------------------------------------------------------
# Users
# ------------------------------------------------------------------------------
class AccountRequest(models.Model):
    business_name = models.CharField(verbose_name='Business Name', max_length=40)
    business_address = models.CharField(verbose_name='Business Address', max_length=75)
    business_city = models.CharField(verbose_name='City', max_length=25, default='')
    business_state = models.CharField(verbose_name='State', max_length=15, default='')
    business_zipcode = models.CharField(verbose_name='Zip Code', max_length=15, default='')
    customer_name = models.CharField(verbose_name='Customer Name', max_length=50)
    customer_position = models.CharField(verbose_name='Job Title', max_length=20)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=13)
    email_address = models.EmailField(verbose_name='Email', max_length=50)
    message_box = models.TextField(
        verbose_name='Message',
        max_length=2000,
        default='',
    )

    def __str__(self):
        return self.business_name


class User(AbstractUser, models.Model):
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    req_info = models.ForeignKey(AccountRequest, on_delete=models.SET_NULL, null=True, blank=True)

    qb_access_token = models.CharField(max_length=2000, null=True, blank=True)
    qb_refresh_token = models.CharField(max_length=500, null=True, blank=True)

# ------------------------------------------------------------------------------
# Quickbooks
# ------------------------------------------------------------------------------


class Bearer:
    def __init__(self, refreshExpiry, accessToken, tokenType, refreshToken, accessTokenExpiry, idToken=None):
        self.refreshExpiry = refreshExpiry
        self.accessToken = accessToken
        self.tokenType = tokenType
        self.refreshToken = refreshToken
        self.accessTokenExpiry = accessTokenExpiry
        self.idToken = idToken
