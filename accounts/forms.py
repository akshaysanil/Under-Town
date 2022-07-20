from dataclasses import field, fields
import imp
from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'placeholder':'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'placeholder':'Confirm Password',
    }))
    class Meta:
        model=Account
        fields=('email','first_name','last_name','phone_no','password')

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)

        self.fields['first_name'].widget.attrs['placeholder']='Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter your Emaiil Adress'
        self.fields['phone_no'].widget.attrs['placeholder']='Enter your Phone Number'

        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match..!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_no')
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)   
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {"invalid": ("Image Files Only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','profile_picture','city','state','country')
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'