from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','username','password1','password2','address','d_o_b','phone_number','gender','image']
    
    def __init__(self, *args, **kwargs):
        # Initialize the form and apply custom styling to fields
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
        
        self.fields['d_o_b'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    
    def clean_phone_number(self):
        # Validate the phone number field
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Enter a valid 10-digit phone number.")
        return phone_number

    def clean_email(self):
        # Validate the email field
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise ValidationError("Enter a valid email address.")
        return email
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file extension
            valid_extensions = ['jpg', 'jpeg', 'png']
            if not image.name.split('.')[-1].lower() in valid_extensions:
                raise ValidationError("Only '.jpg', '.jpeg', and '.png' file formats are allowed.")
        return image
    
    def clean(self):
        # Custom validation for the entire form
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
    

class ProfileEditForm(forms.ModelForm):
    class Meta:
        # Use the custom user model
        model = CustomUser
        # Fields to be displayed in the profile edit form
        fields = ['email', 'username', 'address', 'phone_number','d_o_b','gender','image']
    
    def __init__(self, *args, **kwargs):
        # Initialize the form and apply custom styling to fields
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
        
        self.fields['d_o_b'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
            
    def clean_phone_number(self):
        # Validate the phone number field
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Enter a valid 10-digit phone number.")
        return phone_number
    
    def clean_email(self):
        # Validate the email field
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise ValidationError("Enter a valid email address.")
        return email
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file extension
            valid_extensions = ['jpg', 'jpeg', 'png']
            if not image.name.split('.')[-1].lower() in valid_extensions:
                raise ValidationError("Only '.jpg', '.jpeg', and '.png' file formats are allowed.")
        return image
    