from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import FreshSheet, Order, FoodItem, OrderItem, AccountRequest


def home(request):
    cart_quantities = {}

    if hasattr(request.user, 'cart') and request.user.cart:
        for line_item in request.user.cart.items.all():
            # Need to make the key a str here so in the template we can access it from the str version of pk
            cart_quantities[str(line_item.item.pk)] = line_item.quantity

    return render(request, 'freshsheet/home.html', {
        "freshsheet": FreshSheet.objects.filter(published=True).last(),
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

    # SEND EMAIL TO HUGH
    #send_mail('ORDER CONFIRMATION' + 'Order' + cart.pk, 'Invoice@everfresh.com', ['myersb88@gmail.com'], fail_silently=False)

    # SEND EMAIL TO CUSTOMER
    # ex: send_mail('Subject here', 'Here is the message.', 'Invoice@everfresh.com', ['myersb88@gmail.com'], fail_silently=False)

    html_message = loader.render_to_string('freshsheet/invoice.html', {'invoice': cart})

    send_mail('Order Confirmation', 'Thank you for your order. It\'ll be shipped in a jiffy', 'myersb88@gmail.com', ['myersb88@gmail.com'],
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
    print(order_pk)
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

    print(request.POST)

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

        # # Get recent and non recent food items by doing opposite queries
        # thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        # recent_food_items = FoodItem.objects.filter(date_added__gte=thirty_days_ago)
        # non_recent_food_items = FoodItem.objects.exclude(date_added__gte=thirty_days_ago)
        #
        # # Add recent items to group
        # context['food_item_groups'] = {
        #     'recent': recent_food_items,
        # }
        #
        # for item in non_recent_food_items:
        #     if not context['food_item_groups'][item.category]:
        #         context['food_item_groups'][item.category] = []
        #     context['food_item_groups'][item.category].append(item)
        #
        # return context


# def registration_request(request):
#     if request.method == 'POST':
#         form = RequestAccount(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/thanks/')
#     else:
#         form = RequestAccount()
#     return render(request, 'registration/registration_request.html', {'form': form})
#

def thanks(request):
    return render(request, 'registration/thanks.html')


class RequestAccountCreateView(CreateView):
    model = AccountRequest
    template_name = 'registration/registration_request.html'
    fields = [
        'business_name',
        'business_address',
        'customer_name',
        'customer_position',
        'phone_number',
        'email_address'
    ]
    success_url = reverse_lazy('thanks')


class FreshSheetCreateView(FreshSheetFormViewMixin, CreateView):
    pass


class FreshSheetUpdateView(FreshSheetFormViewMixin, UpdateView):
    pass


class FreshSheetDeleteView(FreshSheetFormViewMixin, DeleteView):
    template_name = 'freshsheet/freshsheet_confirm_delete.html'


