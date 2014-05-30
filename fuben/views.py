from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone


from .models import ComicBook

def index(request):
    context = {}
    comic_books = ComicBook.objects.order_by('?')[:5]    
    context["comic_books"] = comic_books
    return render(request, 'index.html', context)
