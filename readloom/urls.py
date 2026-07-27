"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from django.shortcuts import render
from books.models import Book

def home(request):
    # Get top 8 books by number of reads
    featured_books = Book.objects.all().order_by('-reads')[:8]
    context = {
        'featured_books': featured_books
    }
    return render(request, 'index.html', context)

urlpatterns = [
    path('', home, name='home'),   
    path('admin/', admin.site.urls),
    path('authentication/', include("authentication.urls")),
    path('books/',include("books.urls")),
    path('shelves/',include("shelves.urls")),
]
