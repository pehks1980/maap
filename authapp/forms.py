
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms


from .models import MaapUser


class MaapUserLoginForm(AuthenticationForm):
    class Meta:
        model = MaapUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(MaapUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MaapUserRegisterForm(UserCreationForm):
    class Meta:
        model = MaapUser
        fields = ('username', 'first_name', 'password', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            pass#raise forms.ValidationError("Вы слишком молоды!")

        return data



class MaapUserEditForm(UserChangeForm):
    class Meta:
        model = MaapUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            pass#raise forms.ValidationError("Вы слишком молоды!")

        return data
