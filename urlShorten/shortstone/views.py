from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Url
from django.db import models
from django.shortcuts import render
import random
import string
# Create your views here.
def index(request):

    return render(request, "shortstone/index.html",{"test":"fuck"})
@csrf_exempt
def slug(request, slug):
    if request.method =="GET":
        try:
            url = Url.objects.get(slug=slug)
            return HttpResponseRedirect(url.url)
        except Url.DoesNotExist:
            return HttpResponse("DoesNotExist")
    elif request.method == "POST":
        url = request.POST.get("url")
        slug = request.POST.get("slug")
        if not url:
            return HttpResponse("No Url given",status=400)
        if not url.startswith("https://"):
            url = "https://"+url
        if not slug:
            slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        try:
            Url.objects.get(slug=slug)
            return HttpResponse("Slug is already in use, son",status=400)
        except Url.DoesNotExist:
            url = Url(url=url,slug=slug)
            url.save()
            return HttpResponse("Slug "+url.slug+" has been saved!")
