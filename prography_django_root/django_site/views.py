from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def home_list(request):

    #return HttpResponse("i am sisi")
    return render(request, 'list.html')#, context)


def detail_view(request):

    return render(request, 'detail.html')