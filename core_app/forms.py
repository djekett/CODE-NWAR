from django import forms
from .models import ContactMessage, DownloadRequest, Feedback


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Votre nom complet",
                "class": "form-input",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "votre@email.com",
                "class": "form-input",
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Sujet de votre message",
                "class": "form-input",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Decrivez votre projet ou votre demande...",
                "class": "form-input form-textarea",
                "rows": 5,
            }),
        }


class DownloadRequestForm(forms.ModelForm):
    class Meta:
        model = DownloadRequest
        fields = [
            "full_name", "email", "phone", "profession", "organization",
            "country", "city", "heard_from", "intended_use",
            "accepts_newsletter",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "Ex: Kouassi Yao",
                "class": "form-input", "required": True,
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "votre@email.com",
                "class": "form-input", "required": True,
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+225 07 00 00 00 00",
                "class": "form-input", "required": True,
            }),
            "profession": forms.Select(attrs={"class": "form-input"}),
            "organization": forms.TextInput(attrs={
                "placeholder": "Votre entreprise (optionnel)",
                "class": "form-input",
            }),
            "country": forms.TextInput(attrs={
                "placeholder": "Cote d'Ivoire",
                "class": "form-input", "required": True,
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "Abidjan",
                "class": "form-input",
            }),
            "heard_from": forms.Select(attrs={"class": "form-input"}),
            "intended_use": forms.Textarea(attrs={
                "placeholder": "Ex: Leves topographiques pour des projets de lotissement...",
                "class": "form-input form-textarea", "rows": 3,
            }),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            "full_name", "email", "rating",
            "what_liked", "what_to_improve", "features_wanted",
            "would_recommend",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "Votre nom (optionnel)",
                "class": "form-input",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "votre@email.com (optionnel)",
                "class": "form-input",
            }),
            "rating": forms.Select(attrs={"class": "form-input"}),
            "what_liked": forms.Textarea(attrs={
                "placeholder": "Quelles fonctionnalites vous ont le plus plu ?",
                "class": "form-input form-textarea", "rows": 3,
            }),
            "what_to_improve": forms.Textarea(attrs={
                "placeholder": "Quels aspects devraient etre ameliores ?",
                "class": "form-input form-textarea", "rows": 3,
            }),
            "features_wanted": forms.Textarea(attrs={
                "placeholder": "Quelles nouvelles fonctionnalites aimeriez-vous voir ?",
                "class": "form-input form-textarea", "rows": 3,
            }),
        }
