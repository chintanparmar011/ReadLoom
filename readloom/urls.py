from django.contrib import admin
from django.urls import path, include  
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
