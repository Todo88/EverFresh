from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from datetime import datetime

# Create your models here.

# ------------------------------------------------------------------------------
# Farms Database Input
# ------------------------------------------------------------------------------
from django.template import loader
from django.utils import timezone


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
        if self.unit == 'LB':
            return "Pounds"
        if self.unit == 'BU':
            return "Bundles"
        if self.unit == 'HD':
            return "Heads"
        if self.unit == 'C':
            return "Count"
        else:
            return self.unit

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
        # NOT DRY AT ALL, NEEDS WORK ON LOGIC FOR CONDENSATION.
        if self.item.case_count is None or self.item.wholesale_count is None:
            if self.item.case_count is None and self.item.wholesale_count is None:
                return self.item.price * self.quantity
            if self.item.wholesale_count is not None:
                if self.quantity >= self.item.wholesale_count and self.item.wholesale_count is not None:
                    return self.item.wholesale_price * self.quantity
            if self.item.case_count is not None:
                if self.item.case_count <= self.quantity < self.item.wholesale_count and self.item.case_count is not None:
                    return self.item.case_price * self.quantity
                return self.item.price * self.quantity
            else:
                return self.item.price * self.quantity

        if self.item.case_count is not None and self.item.wholesale_count is not None:
            if self.quantity >= self.item.wholesale_count:
                return self.quantity * self.item.wholesale_price
            if self.item.case_count <= self.quantity < self.item.wholesale_count:
                return self.quantity * self.item.case_price
            if self.quantity < self.item.case_count:
                return self.quantity * self.item.price

    @property
    def unit_cost(self):
        """Based on quantity/wholesale prices"""
        if self.quantity >= self.item.wholesale_count:
            return self.item.wholesale_price
        if self.item.case_count <= self.quantity < self.item.wholesale_count:
            return self.item.case_price
        if self.quantity < self.item.case_count:
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

    def send_to_quickbooks(self):
        from quickbooks import QuickBooks, Oauth2SessionManager
        from quickbooks.objects import (Invoice,
                                        SalesItemLineDetail,
                                        SalesItemLine,
                                        Ref)
        customer = Ref()
        customer.value = 1
        customer.name = self.created_by.get_full_name()
        customer.type = 'Customer'

        line_items = []

        for item in self.items.all():
            line_detail = SalesItemLineDetail()
            line_detail.UnitPrice = item.unit_cost  # in dollars
            line_detail.Qty = item.quantity  # quantity can be decimal

            line = SalesItemLine()
            line.Amount = item.total_cost  # in dollars
            line.SalesItemLineDetail = line_detail

            line_items.append(line)

        invoice = Invoice()
        invoice.CustomerRef = customer
        invoice.Line = line_items

        session_manager = Oauth2SessionManager(
            client_id=settings.QUICKBOOKS_COMPANY_ID,
            client_secret=settings.QUICKBOOKS_SECRET,
            access_token="eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..BjsTIBFjGLHae_XAS8KBYA.E0KUD8n2od3ZRZOzvk6uK_8rz3S6A9Agk2ZwRs9vWnrrPx__8heQl3eFd4yNAdgESb5CB63vHeDW4EGUy9djXKFYAIAWOAci-GHzmoYp1Q8R1TdHIbTRBTCdroMAvTPv3SSC5wiVd3xB4uYa9oUSSs1YKpoqlLynXof_nWMvRgk3td3CiNJUK-0TF5CrzijIb-346vrLnpSeNrwGmHPL-Tfwvu84W7J0nLbzOuZgX4YrhCmz4WhWrZj0IVPBEzPXYMeuysMHd8OQgd5nqSubbtGTtlmVoPrfXftRcRLsVaHoXMePxDHJ3O3nrq3IVBuuiE3IynBu1XWmPlBzRffRlxaB5XPamlPNuELCrSpI0CQQr4mD9ycvqcxw0TceMHefIU2lHnU7x9ua9elrMORmIvW78DfcxvMUVyqWdgF2dyaGpFwqH_eH68KPMh6yDlzN7D6F6l15PAXnzuMuUj3rriuAYRgtdsjeV6bE62j9TMn5FIPGX8j2b4xxJJYROAOBPB-9iy-pTXG823vHwWXaZ-9NgbmWHnGdp14v1PD6Rbo_A7Sx-wGvTOS1F3ExBaNFQE9y_Jt9XJ5eheINolPYbndCImm9rybHozhEnUQ81pQ_P13OvwRHheVxteZ9gPp-HsrdoD1j3P12NXTFCEX2wtfoqeTgkzoAM0Z2H615pWqRQ1l9BMer7t25WKjpjPIzIOtZqPvsnNpme-SPI46Fz-q8dgz7cJuWZm1hshPPdq4.PmzidBmNrD2dqV5zJnjacQ"
        )
        session_manager.start_session()


        client = QuickBooks(
            sandbox=True,
            session_manager=session_manager,
            consumer_key=settings.QUICKBOOKS_CLIENT_ID,
            consumer_secret=settings.QUICKBOOKS_SECRET,
            company_id=settings.QUICKBOOKS_COMPANY_ID,
        )

        invoice.save(qb=client)

    def __str__(self):
        return 'Order #' + str(self.pk)


# ------------------------------------------------------------------------------
# Users
# ------------------------------------------------------------------------------
class User(AbstractUser, models.Model):
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)


class AccountRequest(models.Model):
    business_name = models.CharField(verbose_name='Business Name', max_length=40)
    business_address = models.CharField(verbose_name='Business Address', max_length=75)
    customer_name = models.CharField(verbose_name='Customer Name', max_length=50)
    customer_position = models.CharField(verbose_name='Job Title', max_length=20)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=13)
    email_address = models.EmailField(verbose_name='Email', max_length=50)
    message_box = models.TextField(
        verbose_name='Please leave a message with your needs, questions, etc.',
        max_length=5000,
        default='',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.business_name
