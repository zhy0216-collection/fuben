from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone
# Create your views here.


def index(request):
    
    return render(request, 'test.html', {})
