from django import forms
from schedule.models import Homework


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date']
