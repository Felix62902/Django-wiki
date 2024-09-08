from django import forms

class CreateNewEntry(forms.Form):
    # structure should be same as db
    title = forms.CharField(label="Title", max_length=40, required=True)
    content = forms.CharField(label="Content", max_length=200 ,required=True)
    