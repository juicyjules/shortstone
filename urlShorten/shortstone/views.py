from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
import json
from .models import Url
from django.db import models
from django.shortcuts import render
import random
import string
# Create your views here.
def index(request):

    return render(request, "shortstone/index.html",{"msg":"Create a short, easy to remeber slug to any website!", "submsg":"Leave empty for a random slug","slug":""})
@csrf_exempt
def slug(request, slug):
    if request.method =="GET":
        if(slug=="new"):
            return HttpResponseRedirect("/")
        try:
            url = Url.objects.get(slug=slug)
            return HttpResponseRedirect(url.url)
        except Url.DoesNotExist:
            return render(request, "shortstone/index.html",{"msg":"Slug "+slug+" doesn't exist. Be the first to claim it!","submsg":"Or don't, I can't force you.","slug":slug})
    elif request.method == "POST":
        url = request.POST.get("url")
        validate = URLValidator();
        slug = request.POST.get("slug")
        if not url:
            return HttpResponse("No Url given",status=400)
        if not url.startswith("https://"):
            url = "https://"+url
        try:
            validate(url)
        except:
            return render(request, "shortstone/index.html",{"msg":"Your URL is not an URL.","submsg":"How could you, man...","slug":slug})
        if slug == "new":
                return HttpResponseRedirect("/")
        if not slug:
            slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        try:
            Url.objects.get(slug=slug)
            newSlug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            return render(request, "shortstone/index.html",{"msg":"Slug "+slug+" is already in use. Create a different one!","slug":newSlug})
        except Url.DoesNotExist:
            url = Url(url=url,slug=slug)
            url.save()
            return render(request, "shortstone/stuff.html",{"slug":slug})
