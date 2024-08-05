from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(label='Find the product you want, try to be specific: ', max_length=100)
