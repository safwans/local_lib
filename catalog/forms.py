from django import forms
from django.core.exceptions import ValidationError
import datetime
from datetime import date


class RenewBookForm(forms.Form):
  renewal_date = forms.DateField()
  
  def clean_renewal_date(self):
    data = self.cleaned_data['renewal_date']
    
    if data < date.today():
      raise ValidationError('Invalid Date')
    
    if data > (date.today() + datetime.timedelta(weeks=4)):
      raise ValidationError("Invalid Date - more than 4 weeks")
    
    return data