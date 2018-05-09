from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.template import loader

from .models import FreshSheet, Order, FoodItem, OrderItem


def home(request):
    return render(request, 'freshsheet/home.html')


def index(request):
    # return HttpResponse("You're at the Fresh Sheet index.")

    freshsheets = FreshSheet.objects.all()[:10]

    context = {
        'title': 'Latest Fresh Sheets',
        'freshsheets': freshsheets,
    }
    return render(request, 'freshsheet/index.html', context)


def details(request, id):
    freshsheet = FreshSheet.objects.get(id=id)

    context = {
        'freshsheet': freshsheet,
    }

    return render(request, 'freshsheet/details.html', context)

# details must pass database info to call from database in details.html


@login_required
def cart(request):
    # line_items = request.user.cart.items.all()
    #
    # for line_item in line_items:
    #     line_item.total_cost = line_item.price * line_item.quantity
    #
    # # for line_item in line_items:
    # #     line_item.cart_total += line_item.total_cost
    #
    # context = {
    #     # 'cart': request.user.cart,
    #     'line_items': line_items
    # }

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




