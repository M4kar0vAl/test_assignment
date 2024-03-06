from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File', required=False)


class WordcountForm(forms.Form):
    word = forms.CharField(label='Word to count', required=False)
