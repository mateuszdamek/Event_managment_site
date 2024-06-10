from django import forms
from django.contrib.auth.models import User
from .models import Event

#formularz dla uzytkownika
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


#formularz dla wydarzen
class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'start_date', 'end_date', 'location', 'status', 'organizer_ID', 'parent_event_ID']
        widgets = {
            'parent_event_ID': forms.Select(attrs={'class': 'form-control'}),
        }
        

