from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from betterforms.multiform import MultiModelForm
from django.contrib.auth import get_user_model

from accounts.models import User, Client, Company, Service

class ClientForm(forms.ModelForm):
    statenumber = forms.CharField(label='State Number', widget=forms.TextInput(attrs={"class": 'form-control'}))
    mark = forms.CharField(label='Mark', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    region = forms.CharField(label='Region', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    model = forms.CharField(label='Model', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    class Meta:
        model = Client
        fields = ('statenumber', 'mark', 'region', 'model', 'car_type')


class CompanyForm(forms.ModelForm):
    company_name = forms.CharField(label='Company name', widget=forms.TextInput(attrs={"class": 'form-control'}))
    location = forms.CharField(label='Company on map', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = Company
        fields = ('company_name', 'location',)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('firstname', 'secondname', 'email', 'city')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = True
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": 'form-control'}))
    firstname = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    secondname = forms.CharField(label='Surname', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    city = forms.CharField(label='City', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'firstname', 'secondname', 'city']


class ClientFieldsChangeForm(forms.ModelForm):
    statenumber = forms.CharField(label='State Number', widget=forms.TextInput(attrs={"class": 'form-control'}))
    mark = forms.CharField(label='Mark', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    region = forms.CharField(label='Region', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    model = forms.CharField(label='Model', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    class Meta:
        model = Client
        fields = ['statenumber', 'mark', 'region', 'model', 'car_type']


class CompanyFieldsChangeForm(forms.ModelForm):
    company_name = forms.CharField(label='Company name', widget=forms.TextInput(attrs={"class": 'form-control'}))
    location = forms.CharField(label='Company on map', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    class Meta:
        model = Company
        fields = ['company_name', 'location',]


class ClientCreationMultiForm(MultiModelForm):
    form_classes = {
        'user': RegisterForm,
        'client': ClientForm,
    }


class CompanyCreationMultiForm(MultiModelForm):
    form_classes = {
        'user': RegisterForm,
        'company': CompanyForm,
    }


class ClientEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserDetailChangeForm,
        'client': ClientFieldsChangeForm,
    }


class CompanyEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserDetailChangeForm,
        'company': CompanyFieldsChangeForm,
    }


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email    = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": 'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'input100'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'car_type', 'price', 'example',)
