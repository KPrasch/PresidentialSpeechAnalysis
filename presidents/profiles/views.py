from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Person, President, Speech


class HomeView(TemplateView):
    """
    Landing Page and About.
    """
    template_name = 'presidents.html'


class PresidentListView(ListView):
    """
    Returns a list of all presidents
    """
    model = President
    template_name = 'presidents_list.html'
    context_object_name = 'presidents'


class PresidentDetailView(DetailView):
    """
    Exposes the president object, and a list of reverse related speeches in a list.
    """
    model = President
    template_name = 'president_detail.html'

    def get_context_data(self, **kwargs):
        """
        Adding in the Speeches to the President Detail View.
        """
        context = super().get_context_data(**kwargs)
        context['president'] = context.get('object')
        context['speeches'] = context['president'].speeches.all()
        return context


class SpeechDetailView(DetailView):
    """
    Returns details for one speech record.
    """
    model = Speech
    template_name = 'speech_detail.html'


class SpeechListView(ListView):
    """
    Returns All Speeches.
    """
    model = Speech
    template_name = 'speech_list.html'
    context_object_name = 'speeches'
