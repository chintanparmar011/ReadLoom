from django.db import models
from django.utils.text import slugify
from authentication.models import CustomUser
from PyPDF2 import PdfReader
from django.db.models import Avg
from readloom import settings
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
    RawMediaCloudinaryStorage,
)

class Book(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    CATEGORY_CHOICES = (
        ('science', 'Science & Technology'),
        ('philosophy', 'Philosophy'),
        ('psychology', 'Psychology'),
        ('motivational', 'Motivational'),
        ('fiction', 'Fiction'),
        ('biography', 'Biography'),
        ('history','History'),
        ('mystery & thriller','Mystery & Thriller'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='books'
    )

    book_file = models.FileField(
    upload_to="books/",
    storage=RawMediaCloudinaryStorage()
    )
    cover_image = models.ImageField(
    upload_to="covers/",
    storage=MediaCloudinaryStorage(),
    )
    total_pages = models.IntegerField(default=0,blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_featured = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    unlock_after_books = models.PositiveIntegerField(default=0)

    reads = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        avg = self.ratings.aggregate(avg=Avg('rating'))['avg']
        self.average_rating = round(avg or 0, 1)
        self.save(update_fields=['average_rating'])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Only calculate pages when book is newly uploaded
        if is_new and self.book_file:
            try:
                self.book_file.open("rb")
                reader = PdfReader(self.book_file)
                self.total_pages = len(reader.pages)
                self.book_file.close()

                # update only total_pages (avoid recursion)
                Book.objects.filter(pk=self.pk).update(
                    total_pages=self.total_pages
                )

            except Exception as e:
                print("PDF page count error:", e)

    def __str__(self):
        return self.title
    

class ReadingProgress(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    read_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    last_page = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(default=0)
    progress = models.FloatField(default=0.0)
    reading_seconds = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} → {self.book} ({self.progress:.1f}%)"
    

class BookRating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')  # one rating per user per book

    def __str__(self):
        return f"{self.book.title} - {self.rating}★"
    

class ReadingStreak(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    last_read_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} streak"