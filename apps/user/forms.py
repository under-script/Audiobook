from django import forms


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label="New password", max_length=100)