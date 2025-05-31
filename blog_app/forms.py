# blog_app/forms.py
from django import forms
from .models import Comment
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body') # Fields from the Comment model to include in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Comment'}),
        }
        labels = {
            'name': '',  # Empty label for better placeholder visibility
            'email': '',
            'body': '',
        }