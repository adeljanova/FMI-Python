from django import forms

from exerhealth.accounts.models import FitnessProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = FitnessProfile
        fields = ['height', 'weight', 'age']
