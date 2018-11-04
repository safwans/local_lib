from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Author.objects.create(first_name="Big", last_name="Bob")