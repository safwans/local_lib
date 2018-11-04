from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
  name = models.CharField(max_length=200, help_text="Enter book genre")
  
  class Meta:
    db_table = 'genre'
  
  def __str__(self):
    return self.name

class Author(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField('Died', null=True, blank=True)
  
  class Meta:
    ordering = ['last_name', 'first_name']
    db_table = 'author'
    
  def __str__(self):
    return self.last_name
  
  def get_absolute_url(self):
    return reverse('author-detail', args=[str(self.id)])
  
  
class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
  summary = models.TextField()
  isbn = models.CharField('ISBN', max_length=13)
  genre = models.ManyToManyField(Genre)
  
  class Meta:
    db_table = 'book'
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])
  
class BookInstance(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
  borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  imprint = models.CharField(max_length=200)
  due_back = models.DateField(null=True, blank=True)
  
  LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
  )
  
  status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,
                            default='m')
  
  class Meta:
    ordering = ['due_back']
    db_table = 'book_instance'
    
  def __str__(self):
    return "{} ({})".format(self.id, self.book.title)
  
  @property
  def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False