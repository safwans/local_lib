from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm



# Create your views here.
def index(request):
  num_books = Book.objects.all().count()
  num_instances = Book.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  num_authors = Author.objects.all().count()
  
  # Number of visits to this view, as counted in the session variable.
  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1
  
  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits': num_visits
  }
  
  return render(request, 'catalog/index.html', context=context)
  
class BookListView(generic.ListView):
  #model = Book
  context_object_name = 'book_list'
  #queryset = Book.objects.filter(title__icontains='a')[:5]
  queryset = Book.objects.all()
  template_name = 'book_list.html'
  paginate_by = 1
  
class BookDetailView(generic.DetailView):
    model = Book
    
    


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name ='catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10
    
  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
  
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)
  if request.method == 'POST':
    book_renewal_form = RenewBookForm(request.POST)
    if book_renewal_form.is_valid():
      book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
      book_instance.save()
      return HttpResponseRedirect(reverse('index'))
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    book_renewal_form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
    
  context = {
    'form': book_renewal_form,
    'book_instance': book_instance
  }
    
  return render(request, 'catalog/book_renew_librarian.html', context)