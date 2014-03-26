import datetime

from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, render_to_response
import operator

from shelf.models import Book

# Create your views here.

class HomeView(ListView):
    template_name = 'shelf/home.html'
    model = Book
    queryset = Book.objects.select_related()


def search(request):
    #import pdb; pdb.set_trace()
    user_input = request.GET.get('query').strip()
    results, error = "", ""


    if user_input:
        keywords = user_input.split()
        list_author = [Q(author__icontains=keywords) for keyword in keywords]
        list_title = [Q(title__icontains=keyword) for keyword in keywords]

        final_list = reduce(operator.or_, list_author + list_title)
        results = Book.objects.filter(final_list)

    else:
        error= "You didn't search anything"

    if not results:
        error = "Your search didn't return any results"

        """
        if user_input:
            results = Book.objects.filter(Q(title__icontains=user_input) | Q(author__icontains=user_input))
        else:
            error = 'No results found'
        """
    return render(request, 'shelf/search.html', {"results": results, "error": error})


 

class UpdateBookBaseView(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        book_id = int(kwargs.get('book_id'))

        if book_id:
            self.update_book(book_id)

        return HttpResponseRedirect(reverse('home'))


class CheckoutBookView(UpdateBookBaseView):
    template_name = 'shelf/checkout.html'

    def update_book(self, book_id):
        Book.objects.filter(id=book_id).update(
            borrower=self.request.user,
            last_borrowed_date = datetime.datetime.now()
        )


        

class ReturnBookView(UpdateBookBaseView):
    def update_book(self, book_id):
        Book.objects.filter(id=book_id).update(
            borrower=None)

    

    
