from django import forms

class UploadFileForm(forms.Form):
    datafile = forms.FileField(label='Select a file')