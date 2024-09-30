from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'experience_code', 'dedication_code']
        widgets = {
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'subject_name',
                'placeholder': 'Enter the Subject you are interested in'
            }),
            'experience_code': forms.Select(choices=Subject.ExperienceChoices, attrs={
                'class': 'form-control',
                'id': 'experience-level'
            }),
            'dedication_code': forms.Select(choices=Subject.DedicationChoices, attrs={
                'class': 'form-control',
                'id': 'dedication-level'
            })
        }

    def clean_subject_name(self):
        subject_name = self.cleaned_data['subject_name']
        cleaned_subject_name = ' '.join(subject_name.strip().upper().split())
        return cleaned_subject_name
