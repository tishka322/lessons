from django.shortcuts import render


def platform_index(request):
    return render(request, 'third_task/platform.html')


def catalog(request):
    return render(request, 'third_task/games.html',
                  {'games': ['Atomic Heart',
                             'Cyberpank 2077',
                             'PayDay 2']})


def cart(request):
    return render(request, 'third_task/cart.html')
