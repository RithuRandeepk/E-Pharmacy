from django import forms
from app1.models import Customer
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm


class CustomerProfileform(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','housename','locality','city','mobile','zipcode','state']

        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'housename':forms.TextInput(attrs={'class':'form-control'}),
                 'locality':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'mobile':forms.TextInput(attrs={'class':'form-control'}),
               
                 'zipcode':forms.TextInput(attrs={'class':'form-control'}),
                 'state':forms.Select(attrs={'class':'form-control'})
                 }
# class MyPasswordChangeForm(PasswordChangeForm):

#     old_password=forms.CharField(label='old password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current_password','class':'form-control'}))
#     new_password1=forms.CharField(label='new password',widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control'}))
#     new_password2=forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control'}))

class MyPasswordResetForm(PasswordChangeForm):
    pass


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password-confirmation', 'class': 'form-control'})
    )

class MyPasswordResetForm(PasswordResetForm):

    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):

    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label=' Confirm New Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))



