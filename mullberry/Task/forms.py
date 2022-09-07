from django import forms
from .models import *

class AddTask(forms.Form):
    # nm_Id = forms.CharField(max_length=9, label='Id товара')
    nm_Id = forms.IntegerField(max_value=10**10, label='Артикул товара')
    new_name = forms.CharField(max_length=64, label='Новое название товара')

    def __str__(self):
        # return f" {self.user_name=} {self.item_name=} {self.nmId=} "
        # return str(dir(self))
        return str(self.fields)