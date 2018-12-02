import csv
from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
import logging
import re

from .models import FreshSheet, Order, FoodItem, OrderItem, AccountRequest, Farm, User
import urllib

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings

from freshsheet import getDiscoveryDocument
from .services import (
    getCompanyInfo,
    getBearerTokenFromRefreshToken,
    getUserProfile,
    getBearerToken,
    getSecretKey,
    validateJWTToken,
    revokeToken,
)

from .utils import get_qb_client
from quickbooks.objects.customer import Customer


def home(request):
    freshsheet = FreshSheet.objects.filter(published=True).last()
    cart_quantities = {}
    processed_items = OrderedDict()

    if hasattr(request.user, 'cart') and request.user.cart:
        for line_item in request.user.cart.items.all():
            # Need to make the key a str here so in the template we can access it from the str version of pk
            cart_quantities[str(line_item.item.pk)] = line_item.quantity

    processed_items['Featured'] = []

    for item in freshsheet.items.all().order_by('category'):
        if item.featured:
            category = 'Featured'
        else:
            category = item.category
        if category not in processed_items:
            processed_items[category] = []
        processed_items[category].append(item)

    return render(request, 'freshsheet/home.html', {
        "freshsheet": FreshSheet.objects.filter(published=True).last(),
        "processed_items": processed_items,
        "cart_quantities": cart_quantities,
    })


# details must pass database info to call from database in details.html


@login_required
def cart(request):
    # NOTE: We don't need any context here because request.user.cart has all of the functions
    # and data we need
    return render(request, 'freshsheet/cart.html')


def _add_to_cart(user, item_pk, quantity):
    # Example checks:
    #  - Is the FoodItem expired, maybe? do we have enough quantity to even sell it?
    #  - Is the quantity given > 0?

    # first get the cart, and make one if it doesn't exist
    if not user.cart:
        user.cart = Order.objects.create(status='Pending', created_by=user)
        user.save()

    try:
        item_detail_in_cart = user.cart.items.filter(item__id=item_pk)
        if item_detail_in_cart:
            item_detail_in_cart[0].quantity += quantity
            item_detail_in_cart[0].save()
        else:
            food_item = FoodItem.objects.get(pk=item_pk)
            OrderItem.objects.create(
                order=user.cart,
                item=food_item,
                price=food_item.price,
                quantity=quantity
            )
        return True

    except ObjectDoesNotExist:
        return False


@login_required
def add_to_cart_view(request, item_pk, quantity):
    # You want this in the future to prevent someone from sending a GET request to add an item
    # if request.method is not 'POST':
    #     raise Http404()
    result = _add_to_cart(request.user, item_pk, quantity)
    if result:
        return HttpResponse()
    else:
        raise Http404


@login_required
def remove_from_cart(request, line_item_pk):
    #     Check if item_pk is in current user's cart
    if not request.user.cart.items.filter(pk=line_item_pk).exists():
        raise PermissionDenied("You can't delete things not in your own cart")

    request.user.cart.items.filter(pk=line_item_pk).delete()

    return redirect('/cart/')


@login_required
def update_cart(request):
    errors = {}

    item_pks_and_quantities = []
    for line_item_pk, value in request.POST.items():
        if line_item_pk.startswith('quantity_'):
            pk = line_item_pk.replace("quantity_", "")
            try:
                value = abs(int(value))

                if value > 0:
                    item_pks_and_quantities.append((pk, value))
                else:
                    errors[pk] = 'Quantity of ' + str(OrderItem.objects.get(pk=pk).item) + \
                                 ' was not valid. It has been set to its previous quantity.'

            except ValueError:
                errors[pk] = "'{}' is not a valid input for this field".format(value)

    print(errors)

    # If we have no errors, then save all of the goods
    for pk, value in item_pks_and_quantities:
        if request.user.cart.items.filter(pk=pk):
            OrderItem.objects.filter(pk=pk).update(quantity=value)

    return render(request, 'freshsheet/cart.html', {"errors": errors})


@login_required
def checkout(request):
    if request.user.cart is None:
        return redirect('/')

    # Remove from cart
    # request.user.cart = request.user.cart().delete()
    # request.user.cart = Order.objects.create(status='Pending', created_by=request.user)
    cart = request.user.cart
    cart.status = "Pending"
    cart.save()

    cart.send_to_quickbooks(request)

    # SEND EMAIL TO HUGH
    # send_mail('ORDER CONFIRMATION' + 'Order' + cart.pk, 'Invoice@everfresh.com', ['myersb88@gmail.com'], fail_silently=False)

    # SEND EMAIL TO CUSTOMER
    # ex: send_mail('Subject here', 'Here is the message.', 'Invoice@everfresh.com', ['myersb88@gmail.com'], fail_silently=False)

    html_message = loader.render_to_string('freshsheet/invoice.html', {'invoice': cart})

    send_mail('Order Confirmation', 'Thank you for your order. It\'ll be shipped in a jiffy', 'myersb88@gmail.com',
              ['myersb88@gmail.com'],
              fail_silently=False, html_message=html_message)

    request.user.cart = None
    request.user.save()

    # Send email
    print('Send Email Here')
    # return redirect(request, 'invoice')
    return redirect(reverse('invoice', kwargs={"order_pk": cart.pk}))
    # return HttpResponseRedirect(reverse('invoice', kwargs={"order_pk": request.user.cart.pk}))


@login_required
def invoice(request, order_pk):
    # Make sure the ONLY person who owns this invoice or ADMIN can view this
    try:
        invoice = Order.objects.get(pk=order_pk)
        return render(request, 'freshsheet/invoice.html', {"invoice": invoice})
    except ObjectDoesNotExist:
        return Http404()


@login_required()
def add_line_items_to_cart(request):
    """
    What we're going to receive:
        form_elements is our list of elements (maybe in request.POST?)

        for element in form_elements:
            food_item_pk = element.name.split("food_item_")[1]
            food_item = FoodItem.objects.get(pk=food_item_pk)
            new_line_item = LineItem.objects.create(food_item=food_item, quantity=element.value)
            request.user.cart.items.add(new_line_item)
    """

    for name, value in request.POST.items():
        try:
            value = int(value)
        except ValueError:
            continue
        if "food_item_" in name and value:
            food_item_pk = name.split("food_item_")[1]
            _add_to_cart(request.user, food_item_pk, value)

    return HttpResponseRedirect(reverse('cart'))


# -----------------------------------------------------------------------------
# Freshsheets
# -----------------------------------------------------------------------------


def list_freshsheets(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied()

    freshsheets = FreshSheet.objects.all()[:10]

    context = {
        'title': 'Latest Fresh Sheets',
        'freshsheets': freshsheets,
    }
    return render(request, 'freshsheet/index.html', context)


def details(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied()

    freshsheet = FreshSheet.objects.get(id=id)

    context = {
        'freshsheet': freshsheet,
    }

    return render(request, 'freshsheet/details.html', context)


def publish(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied()

    freshsheet = FreshSheet.objects.get(pk=pk)
    if freshsheet.published:
        return PermissionDenied("Cannot republish a freshsheet!")
    freshsheet.published = True
    freshsheet.save()
    return HttpResponseRedirect(reverse("list_freshsheets"))


class FreshSheetFormViewMixin:
    model = FreshSheet
    template_name = 'freshsheet/freshsheet_form.html'
    fields = ['greeting', 'items']
    success_url = reverse_lazy('list_freshsheets')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['food_item_groups'] = {}

        food_items = FoodItem.objects.all()
        for item in food_items:
            if item.category not in context['food_item_groups']:
                context['food_item_groups'][item.category] = []
            context['food_item_groups'][item.category].append(item)

        return context


# def registration_request(request):
#     if request.method == 'POST':
#         form = RequestAccount(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/thanks/')
#     else:
#         form = RequestAccount()
#     return render(request, 'registration/registration_request.html', {'form': form})
#

def management(request):
    return render(request, 'management.html')


def thanks(request):
    return render(request, 'registration/thanks.html')


class RequestAccountCreateView(CreateView):
    model = AccountRequest
    template_name = 'registration/registration_request.html'
    fields = [
        'business_name',
        'business_address',
        'business_city',
        'business_state',
        'business_zipcode',
        'customer_name',
        'customer_position',
        'phone_number',
        'email_address',
        'message_box',
    ]
    success_url = reverse_lazy('thanks')


class FreshSheetCreateView(FreshSheetFormViewMixin, CreateView):
    pass


class FreshSheetUpdateView(FreshSheetFormViewMixin, UpdateView):
    pass


class FreshSheetDeleteView(FreshSheetFormViewMixin, DeleteView):
    template_name = 'freshsheet/freshsheet_confirm_delete.html'


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "freshsheet/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("list_freshsheets"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("list_freshsheets"))

        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)
        for row in reader:

            farm, _ = Farm.objects.get_or_create(name=row['Farm'])

            defaults = {
                "unit": row['Unit'],
                "price": row['Each'],
                "category": row['Category'],
                "account": row['Account'],
                "type": row['Type'],
                "farm": farm,
            }

            if 'Split' in row and row['Split']:
                defaults["case_price"] = row['Split']

            if 'SP/TH' in row and row['SP/TH']:
                defaults["case_count"] = row['SP/TH']

            if 'Case' in row and row['Case']:
                defaults["wholesale_price"] = row['Case']

            if 'CA/TH' in row and row['CA/TH']:
                defaults["wholesale_count"] = row['CA/TH']

            FoodItem.objects.update_or_create(
                name=row['Item Name'],
                defaults=defaults,
            )

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("list_freshsheets"))


# ------------------------------------------
#               QUICKBOOKS
# ------------------------------------------


def importUsersFromQuickbooks(request):
    client = get_qb_client()
    customers = Customer.all(qb=client)

    for customer in customers:
        result, created = User.objects.update_or_create(
            defaults={
                'email': customer.PrimaryEmailAddr.Address if customer.PrimaryEmailAddr else '',
                'first_name': customer.GivenName,
                'last_name': customer.FamilyName,
                'username': customer.GivenName + customer.FamilyName + customer.Id,
            },
            qb_customer_id=customer.Id,
        )

    return render(request, 'management.html')


def connectToQuickbooks(request):
    url = getDiscoveryDocument.auth_endpoint
    params = {'scope': settings.ACCOUNTING_SCOPE, 'redirect_uri': settings.REDIRECT_URI,
              'response_type': 'code', 'state': get_CSRF_token(request), 'client_id': settings.CLIENT_ID}
    url += '?' + urllib.parse.urlencode(params)
    return redirect(url)


def signInWithIntuit(request):
    url = getDiscoveryDocument.auth_endpoint
    scope = ' '.join(settings.OPENID_SCOPES)  # Scopes are required to be sent delimited by a space
    params = {'scope': scope, 'redirect_uri': settings.REDIRECT_URI,
              'response_type': 'code', 'state': get_CSRF_token(request), 'client_id': settings.CLIENT_ID}
    url += '?' + urllib.parse.urlencode(params)
    return redirect(url)


def getAppNow(request):
    url = getDiscoveryDocument.auth_endpoint
    scope = ' '.join(settings.GET_APP_SCOPES)  # Scopes are required to be sent delimited by a space
    params = {'scope': scope, 'redirect_uri': settings.REDIRECT_URI,
              'response_type': 'code', 'state': get_CSRF_token(request), 'client_id': settings.CLIENT_ID}
    url += '?' + urllib.parse.urlencode(params)
    return redirect(url)


def authCodeHandler(request):
    state = request.GET.get('state', None)
    error = request.GET.get('error', None)
    if error == 'access_denied':
        return redirect('home')
    if state is None:
        return HttpResponseBadRequest()
    elif state != get_CSRF_token(request):  # validate against CSRF attacks
        return HttpResponse('unauthorized', status=401)

    auth_code = request.GET.get('code', None)
    if auth_code is None:
        return HttpResponseBadRequest()

    bearer = getBearerToken(auth_code)
    realmId = request.GET.get('realmId', None)
    updateSession(request, bearer.accessToken, bearer.refreshToken, realmId)

    # Validate JWT tokens only for OpenID scope
    if bearer.idToken is not None:
        if not validateJWTToken(bearer.idToken):
            return HttpResponse('JWT Validation failed. Please try signing in again.')
        else:
            return redirect('connected')
    else:
        return redirect('connected')


def connected(request):
    access_token = request.session.get('accessToken', None)
    if access_token is None:
        return HttpResponse('Your Bearer token has expired, please initiate Sign In With Intuit flow again')
    refresh_token = request.session.get('refreshToken', None)

    request.user.qb_access_token = access_token
    request.user.qb_refresh_token = refresh_token
    request.user.save()

    return render(request, 'connected.html')


def disconnect(request):
    access_token = request.session.get('accessToken', None)
    refresh_token = request.session.get('refreshToken', None)

    revoke_response = ''
    if access_token is not None:
        revoke_response = revokeToken(access_token)
    elif refresh_token is not None:
        revoke_response = revokeToken(refresh_token)
    else:
        return HttpResponse('No accessToken or refreshToken found, Please connect again')

    request.session.flush()
    return HttpResponse(revoke_response)


def refreshTokenCall(request):
    refresh_token = request.session.get('refreshToken', None)
    if refresh_token is None:
        return HttpResponse('Not authorized')
    bearer = getBearerTokenFromRefreshToken(refresh_token)

    if isinstance(bearer, str):
        return HttpResponse(bearer)
    else:
        return HttpResponse('Access Token: ' + bearer.accessToken + ', Refresh Token: ' + bearer.refreshToken)

#
# def apiCall(request):
#     access_token = request.session.get('accessToken', None)
#     if access_token is None:
#         return HttpResponse('Your Bearer token has expired, please initiate C2QB flow again')
#
#     realmId = request.session['realmId']
#     if realmId is None:
#         return HttpResponse('No realm ID. QBO calls only work if the accounting scope was passed!')
#
#     refresh_token = request.session['refreshToken']
#     company_info_response, status_code = getCompanyInfo(access_token, realmId)
#
#     if status_code >= 400:
#         # if call to QBO doesn't succeed then get a new bearer token from refresh token and try again
#         bearer = getBearerTokenFromRefreshToken(refresh_token)
#         updateSession(request, bearer.accessToken, bearer.refreshToken, realmId)
#         company_info_response, status_code = getCompanyInfo(bearer.accessToken, realmId)
#         if status_code >= 400:
#             return HttpResponseServerError()
#     company_name = company_info_response['CompanyInfo']['CompanyName']
#     address = company_info_response['CompanyInfo']['CompanyAddr']
#     return HttpResponse('Company Name: ' + company_name + ', Company Address: ' + address['Line1'] + ', ' + address[
#         'City'] + ', ' + ' ' + address['PostalCode'])


def get_CSRF_token(request):
    token = request.session.get('csrfToken', None)
    if token is None:
        token = getSecretKey()
        request.session['csrfToken'] = token
    return token


def updateSession(request, access_token, refresh_token, realmId, name=None):
    request.session['accessToken'] = access_token
    request.session['refreshToken'] = refresh_token
    request.session['realmId'] = realmId
    request.session['name'] = name
