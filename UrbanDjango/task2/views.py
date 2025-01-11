from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class Class_view(TemplateView):
    template_name = 'second_task/class_template.html'


def func_view(request):
    return render(request, 'second_task/func_template.html')
