from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'age', 'photo']

    # Field-level validation for age
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            return age
        if age < 5:
            raise forms.ValidationError("Age must be at least 5.")
        return age

    # Whole-form validation (e.g., business rule)
    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name', '')
        last = cleaned.get('last_name', '')
        if first and last and first.lower() == last.lower():
            raise forms.ValidationError("First and last names cannot be identical.")
        return cleaned