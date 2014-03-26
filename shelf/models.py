import json

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from amazon.api import AmazonAPI


class Book(models.Model):
    title = models.CharField(max_length=512, unique=True)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.SmallIntegerField()
    author = models.CharField(max_length=256)
    borrower = models.ForeignKey(User, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_borrowed_date = models.DateTimeField(null=True, blank=True)
    image_url = models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.title, self.author)

    def save(self, *args, **kwargs):
        #is_new = self.id < 1
        is_new = True
        super(Book, self).save(*args, **kwargs)
        if not is_new:
            return
        amazon = AmazonAPI(
            settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY,
            settings.AMAZON_ASSOC_TAG)
        books = amazon.lookup(
            IdType='ISBN', ItemId=self.isbn, SearchIndex='All')
        if books:
            if isinstance(books, list):
                book = books[0]
            else:
                book = books
            Book.objects.filter(pk=self.pk).update(
                title=book.title,
                author=', '.join(book.authors),
                image_url=book.large_image_url)
