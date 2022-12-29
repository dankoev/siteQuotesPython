from django.forms import ModelForm, TextInput, Textarea
from .models import Quotes, KeysWords


class KeysWordsForm(ModelForm):
    class Meta:
        model = KeysWords
        fields = ('keyword',)
        widgets = {
            "keyword": TextInput(attrs={
                'list': 'keywords',
                'class': 'form-control',
                'placeholder': 'Введите ключевое слово'
            })
        }


class QuotesForm(ModelForm):
    class Meta:
        model = Quotes
        fields = ("author", "content")
        widgets = {
            "author": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите автора'
            }),
            "content": Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Введите цитату'
            }),
        }