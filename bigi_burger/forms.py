from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Tailwind CSS classes to form fields and widgets
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full p-2 mb-3 rounded-md shadow-md focus:ring-2 focus:ring-blue-500'})

        # Add specific Tailwind classes for individual fields (if needed)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name', 'class': 'text-gray-700'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name', 'class': 'text-gray-700'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone Number', 'class': 'text-gray-700'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Address', 'class': 'text-gray-700'})

