# blog_app/forms.py
from django import forms
from .models import Comment
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
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

    # New clean method for the honeypot field
    def clean_honeypot(self):
        # If a bot fills this field, it's spam. If a human submitted, it would be empty.
        if self.cleaned_data['honeypot']:
            raise forms.ValidationError("Spam detected. This field should be empty.") # <--- ADD THIS CLEAN METHOD
        return self.cleaned_data['honeypot']