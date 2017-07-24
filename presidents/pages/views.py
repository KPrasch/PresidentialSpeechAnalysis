from django.shortcuts import render
from profiles.models import President

# Create your views here.

def home(request):
    '''
    landing page
    '''
    presidents = President.objects.order_by('-presidency_number')
    context = {'presidents': presidents}
    return render(request, 'pages/home.html', context)

def president_profile(request, slug):
    president = President.objects.get(slug=slug)
