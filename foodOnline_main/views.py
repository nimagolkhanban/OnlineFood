from django.shortcuts import redirect,render
from django.http import HttpRequest, HttpResponse
from django.views import View

class Home(View):
    def get(self, request):
        return render(request, "home.html")