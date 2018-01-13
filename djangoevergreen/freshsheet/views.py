from django.shortcuts import render
from django.http import HttpResponse

from .models import FreshSheet


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

    # print(dir(freshsheet))





    # pip install ipdb then run this, this drops you into an interactive "debugger"
    # where you can check what variables actually are and play with them easily
    # pdb; pdb.set_trace()



    # vegetable = Vegetable.objects.order_by('')[:5]
    # vegetable = freshsheet.vegetables.all.order_by('name')[:5]
    context = {
        'freshsheet': freshsheet,
    }

    return render(request, 'freshsheet/details.html', context)

# details must pass database info to call from database in details.html


def cart(request):

    return render(request, 'freshsheet/cart.html')