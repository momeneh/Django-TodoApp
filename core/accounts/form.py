from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from .models import User


class RegistrationForm(forms.ModelForm):

    password_confirmation = forms.CharField(
        max_length=255, required=True, widget=forms.PasswordInput
    )
    password = forms.CharField(
        max_length=255, required=True, widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "password", "password_confirmation"]

    def clean(self):
        password = self.cleaned_data["password"]
        password_confirmation = self.cleaned_data["password_confirmation"]
        if password != password_confirmation:
            raise ValidationError("passwords dont match")

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise ValidationError(list(e.messages))

        self.cleaned_data.pop("password_confirmation", None)
        return super().clean()

    def save(self, commit=...):
        # super().send_email(self.cleaned_data)
        return User.objects.create_user(**self.cleaned_data)
