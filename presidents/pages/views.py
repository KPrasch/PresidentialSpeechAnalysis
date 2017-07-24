from django.shortcuts import render
from profiles.models import President, Speech

# Create your views here.

def home(request):
    '''
    landing page
    '''
    presidents = President.objects.order_by('-presidency_number')
    num_presidents = presidents.count() + 1 # TODO: find a better way to fix this.
    num_speeches = Speech.objects.count()

    context = {
        'presidents': presidents,
        'num_presidents':num_presidents,
        'num_speeches': num_speeches
    }

    return render(request, 'pages/home.html', context)


def president_profile(request, slug):
    president = President.objects.get(slug=slug)
    speeches = president.speeches.all()  # the reverse foreign key lookup

    context = {'president': president, 'speeches': speeches}
    return render(request, 'pages/president_detail.html', context)
